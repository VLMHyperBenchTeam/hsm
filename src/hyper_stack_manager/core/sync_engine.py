import logging
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from ..models import LibraryManifest, ServiceManifest
from ..manifest import HSMProjectManifest
from ..adapters.base import BasePackageManagerAdapter, BaseContainerAdapter

logger = logging.getLogger(__name__)

class SyncEngine:
    """Handles dependency resolution and environment synchronization."""

    def __init__(self, project_root: Path, manifest: HSMProjectManifest, 
                 registry_path: Path, package_adapter: BasePackageManagerAdapter,
                 container_adapter: BaseContainerAdapter):
        self.project_root = project_root
        self.manifest = manifest
        self.registry_path = registry_path
        self.package_adapter = package_adapter
        self.container_adapter = container_adapter

    def _parse_env_file(self, env_file: Path) -> Dict[str, str]:
        """Parse .env file with strict validation and deterministic behavior."""
        if not env_file.exists():
            raise FileNotFoundError(f"env_file not found: {env_file}")

        parsed: Dict[str, str] = {}
        with env_file.open("r", encoding="utf-8") as f:
            for line_number, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(
                        f"Invalid env file format at {env_file}:{line_number}: '{line}'"
                    )
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    raise ValueError(
                        f"Invalid env file format at {env_file}:{line_number}: empty key"
                    )
                if key in parsed:
                    raise ValueError(
                        f"Duplicate key '{key}' inside env_file '{env_file}'"
                    )
                parsed[key] = value

        return parsed

    def _resolve_profile_name_for_service(self, name: str) -> str:
        """Resolve active profile for service from project manifest."""
        for g_cfg in self.manifest.service_groups.values():
            selection = g_cfg.get("selection")
            if selection == name or (isinstance(selection, (list, tuple)) and name in selection):
                return g_cfg.get("profile") or "default"

        srvs = self.manifest.data.get("services", {}).get("standalone", [])
        for srv in srvs:
            if isinstance(srv, dict) and srv.get("name") == name:
                return srv.get("profile") or "default"

        return "default"

    def _resolve_active_source(self, manifest: ServiceManifest, name: str):
        mode = self.manifest.get_mode(name)
        return manifest.sources.dev if mode == "dev" and manifest.sources.dev else manifest.sources.prod

    def _resolve_service_env_file_chain(self, manifest: ServiceManifest, source: Optional[Any]) -> List[str]:
        """Resolve active env_file chain for service according to mode/profile/source."""
        chain: List[str] = []
        chain.extend(manifest.env_file)
        if source and hasattr(source, "env_file"):
            chain.extend(source.env_file)

        seen = set()
        deduped: List[str] = []
        for p in chain:
            if p not in seen:
                deduped.append(p)
                seen.add(p)
        return deduped

    def _materialize_service_env(
        self,
        name: str,
        env_file_paths: List[str],
        manifest_env: Dict[str, str],
        source_env: Dict[str, str],
        implied_env: Dict[str, str],
    ) -> Tuple[Dict[str, str], Optional[str]]:
        """Build final env with fail-fast conflict checks and materialize project .env file."""

        def _merge_without_override(
            target: Dict[str, str],
            source_data: Dict[str, str],
            source_label: str,
            origins: Dict[str, str],
        ):
            for key, value in source_data.items():
                if key in target:
                    raise ValueError(
                        f"env conflict for service '{name}': key '{key}' is defined in both "
                        f"{origins[key]} and {source_label}"
                    )
                target[key] = str(value)
                origins[key] = source_label

        final_env: Dict[str, str] = {}
        origins: Dict[str, str] = {}

        for path_str in env_file_paths:
            env_path = Path(path_str)
            if not env_path.is_absolute():
                env_path = (self.project_root / env_path).resolve()
            parsed = self._parse_env_file(env_path)
            _merge_without_override(final_env, parsed, f"env_file:{env_path}", origins)

        _merge_without_override(final_env, manifest_env, "manifest.env", origins)
        _merge_without_override(final_env, source_env, "source.env", origins)
        _merge_without_override(final_env, implied_env, "implies.params", origins)

        if not final_env:
            return final_env, None

        env_output = self.project_root / f".env.{name}"
        with env_output.open("w", encoding="utf-8") as f:
            for key in sorted(final_env.keys()):
                f.write(f"{key}={final_env[key]}\n")

        return final_env, str(env_output.relative_to(self.project_root))

    def sync(self, frozen: bool = False):
        """Sync project state with the manifest."""
        logger.info("Starting HSM sync...")
        
        packages_to_sync = {} # Use dict to ensure uniqueness by name
        containers_to_sync = []
        
        # Implication Merging: registry_id -> list of params
        merged_implies_params: Dict[str, List[Dict[str, Any]]] = {}

        def collect_implies(implies: Dict[str, Any]):
            for target, config in implies.items():
                params = {}
                if isinstance(config, dict):
                    params = config.get("params", {})
                
                if target not in merged_implies_params:
                    merged_implies_params[target] = []
                merged_implies_params[target].append(params)

        # 1. Resolve libraries from groups
        for group_name, group_cfg in self.manifest.library_groups.items():
            selection = group_cfg.get("selection")
            if not selection:
                continue
                
            selections = [selection] if isinstance(selection, str) else selection
            
            for pkg_name in selections:
                pkg_req = self._resolve_package_requirement(pkg_name)
                if pkg_req:
                    packages_to_sync[pkg_name] = pkg_req
                    # Collect implies from group selection
                    group_path = self.registry_path / "library_groups" / f"{group_name}.yaml"
                    if group_path.exists():
                        with open(group_path, "r") as f:
                            g_data = yaml.safe_load(f)
                            opt = next((o for o in g_data.get("options", []) if o["name"] == pkg_name), None)
                            if opt and "implies" in opt:
                                collect_implies(opt["implies"])

        # 2. Resolve standalone libraries
        for pkg_name in self.manifest.libraries:
            pkg_req = self._resolve_package_requirement(pkg_name)
            if pkg_req:
                packages_to_sync[pkg_name] = pkg_req
                # Collect implies from standalone library
                pkg_manifest_path = self.registry_path / "libraries" / f"{pkg_name}.yaml"
                if pkg_manifest_path.exists():
                    with open(pkg_manifest_path, "r") as f:
                        p_data = yaml.safe_load(f)
                        if "implies" in p_data:
                            collect_implies(p_data["implies"])

        # 3. Resolve services from groups
        for group_name, group_cfg in self.manifest.service_groups.items():
            selection = group_cfg.get("selection")
            if not selection:
                continue
            selections = [selection] if isinstance(selection, str) else selection
            for cont_name in selections:
                cont_cfg = self._resolve_container_config(cont_name)
                if cont_cfg:
                    containers_to_sync.append(cont_cfg)
                
                # Collect implies from service group selection
                group_path = self.registry_path / "service_groups" / f"{group_name}.yaml"
                if group_path.exists():
                    with open(group_path, "r") as f:
                        g_data = yaml.safe_load(f)
                        opt = next((o for o in g_data.get("options", []) if o["name"] == cont_name), None)
                        if opt and "implies" in opt:
                            collect_implies(opt["implies"])

        # 4. Resolve standalone services
        for cont_name in self.manifest.services:
            cont_cfg = self._resolve_container_config(cont_name)
            if cont_cfg:
                containers_to_sync.append(cont_cfg)
            
            # Collect implies from standalone service
            svc_manifest_path = self.registry_path / "services" / f"{cont_name}.yaml"
            if svc_manifest_path.exists():
                with open(svc_manifest_path, "r") as f:
                    s_data = yaml.safe_load(f)
                    if "implies" in s_data:
                        collect_implies(s_data["implies"])

        # 4.5 Process Merged Implies
        for target, params_list in merged_implies_params.items():
            if ":" in target:
                target_type, target_name = target.split(":", 1)
                if target_type == "service":
                    # Merge params
                    merged_params = {}
                    for p in params_list:
                        for k, v in p.items():
                            if k not in merged_params:
                                merged_params[k] = []
                            if v not in merged_params[k]:
                                merged_params[k].append(v)
                    
                    # Resolve container with merged params
                    cont_cfg = self._resolve_container_config(target_name, merged_params)
                    if cont_cfg:
                        containers_to_sync.append(cont_cfg)

        # 5. Delegate to adapter for packages
        if packages_to_sync:
            self.package_adapter.sync(list(packages_to_sync.values()), frozen=frozen)
        
        # 6. Handle Isolated Services (VES)
        self._sync_isolated_services(frozen=frozen, merged_implies=merged_implies_params)

        # 7. Generate docker-compose.hsm.yml
        if containers_to_sync:
            self.container_adapter.generate_config(containers_to_sync)
            logger.info("Docker Compose manifest generated.")
        else:
            # If no containers, ensure the file is removed to avoid confusion
            compose_path = self.project_root / "docker-compose.hsm.yml"
            if compose_path.exists():
                compose_path.unlink()

        logger.info("Sync completed successfully.")

    def _sync_isolated_services(self, frozen: bool = False, merged_implies: Optional[Dict[str, List[Dict[str, Any]]]] = None):
        """Sync dependencies for isolated services (uv, pixi, etc.)."""
        # 1. Collect all services from manifest
        services_to_check = []
        
        # Standalone services
        for srv in self.manifest.data.get("services", {}).get("standalone", []):
            if isinstance(srv, str):
                services_to_check.append(srv)
            elif isinstance(srv, dict):
                services_to_check.append(srv.get("name"))

        # Group services
        for group_cfg in self.manifest.service_groups.values():
            selection = group_cfg.get("selection")
            if selection:
                if isinstance(selection, str):
                    services_to_check.append(selection)
                else:
                    services_to_check.extend(selection)
        
        # Add services from merged implies (if they are not in the project yet)
        if merged_implies:
            for target in merged_implies:
                if target.startswith("service:"):
                    services_to_check.append(target.split(":", 1)[1])

        logger.debug(f"Services to check for VES sync: {services_to_check}")

        # 2. Resolve all services to ensure we have their manifests and profiles
        for name in set(services_to_check):
            logger.debug(f"Processing service for VES sync: {name}")
            cont_path = self.registry_path / "services" / f"{name}.yaml"
            if not cont_path.exists():
                logger.debug(f"Service manifest not found for '{name}' at {cont_path}")
                continue

            with open(cont_path, "r") as f:
                data = yaml.safe_load(f)
                manifest = ServiceManifest(**data)

            profile_name = self._resolve_profile_name_for_service(name)
            
            if profile_name in manifest.deployment_profiles:
                profile = manifest.deployment_profiles[profile_name]
                logger.debug(f"Service '{name}' profile '{profile_name}' runtime: {profile.runtime}")
                if profile.runtime == "uv":
                    mode = self.manifest.get_mode(name)
                    logger.debug(f"Service '{name}' mode: {mode}")
                    source = self._resolve_active_source(manifest, name)
                    logger.debug(f"Service '{name}' selected source: {source}")
                    
                    implied_env: Dict[str, str] = {}
                    if merged_implies:
                        target_key = f"service:{name}"
                        if target_key in merged_implies:
                            for params in merged_implies[target_key]:
                                for key, values in params.items():
                                    if isinstance(values, list):
                                        implied_env[key] = ",".join(map(str, values))
                                    else:
                                        implied_env[key] = str(values)

                    env_file_chain = self._resolve_service_env_file_chain(manifest, source)
                    service_env, materialized_env_file = self._materialize_service_env(
                        name=name,
                        env_file_paths=env_file_chain,
                        manifest_env=manifest.env,
                        source_env=source.env if source else {},
                        implied_env=implied_env,
                    )

                    if source:
                        path = None
                        if source.type in ["local", "build"]:
                            path = Path(source.path)
                            logger.debug(f"Service '{name}' source type is {source.type}: {path}")
                        elif source.type == "git":
                            path = Path("services") / name
                            logger.debug(f"Service '{name}' source type is git. Target path: {path}")
                            if not (self.project_root / path).exists():
                                # Ensure parent directory exists
                                (self.project_root / path).parent.mkdir(parents=True, exist_ok=True)
                                logger.info(f"Cloning service '{name}' from {source.url} to {self.project_root / path}...")
                                import subprocess
                                cmd = ["git", "clone", source.url, str(self.project_root / path)]
                                if source.ref:
                                    cmd.extend(["-b", source.ref])
                                logger.debug(f"Executing clone command: {' '.join(cmd)}")
                                subprocess.run(cmd, check=True)
                        
                        if path:
                            if not path.is_absolute():
                                path = (self.project_root / path).resolve()
                            
                            logger.debug(f"Resolved absolute path for service '{name}': {path}")
                            
                            if path.exists():
                                logger.info(f"Syncing isolated service '{name}' at {path}...")

                                logger.debug(f"Initial service env for '{name}': {service_env}")
                                
                                # Collect dependencies for the service
                                service_packages = []
                                
                                # 1. Direct dependencies from manifest
                                for dep in manifest.dependencies:
                                    dep_name = dep if isinstance(dep, str) else dep.name
                                    logger.debug(f"Resolving dependency '{dep_name}' for service '{name}'")
                                    pkg_req = self._resolve_package_requirement(dep_name)
                                    if pkg_req:
                                        service_packages.append(pkg_req)
                                        logger.debug(f"Resolved '{dep_name}' to '{pkg_req}'")
                                    else:
                                        # Fallback to simple name if not in registry
                                        req = dep if isinstance(dep, str) else f"{dep.name}=={dep.version}"
                                        service_packages.append(req)
                                        logger.debug(f"Dependency '{dep_name}' not in registry, using: {req}")

                                # 2. Dependencies from library groups in service
                                # (Recursive logic: service can have its own groups)
                                # TODO: Implement recursive group resolution if needed

                                logger.debug(f"Final service env for '{name}': {service_env}")
                                logger.debug(f"Final service packages for '{name}': {service_packages}")
                                
                                if hasattr(self.package_adapter, "sync_service"):
                                    self.package_adapter.sync_service(
                                        path,
                                        service_packages,
                                        frozen=frozen,
                                        env_vars=service_env,
                                        env_file=materialized_env_file,
                                    )

    def _resolve_package_requirement(self, name: str) -> Optional[str]:
        """Resolve a library name to a requirement string."""
        pkg_path = self.registry_path / "libraries" / f"{name}.yaml"
        if not pkg_path.exists():
            logger.warning(f"Library {name} not found in registry")
            return None

        with open(pkg_path, "r") as f:
            data = yaml.safe_load(f)
            manifest = LibraryManifest(**data)
        
        mode = self.manifest.get_mode(name)
        source = manifest.sources.dev if mode == "dev" and manifest.sources.dev else manifest.sources.prod
        
        if not source:
            return None

        if source.type == "local":
            path = Path(source.path)
            if not path.is_absolute():
                path = self.project_root / path
            return f"{name} @ {path.as_uri()}"
        elif source.type == "git":
            req = f"{name} @ git+{source.url}"
            if source.ref:
                req += f"@{source.ref}"
            return req
        
        return None

    def _resolve_container_config(self, name: str, merged_params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Resolve a service name to a docker-compose service config."""
        cont_path = self.registry_path / "services" / f"{name}.yaml"
        if not cont_path.exists():
            logger.warning(f"Service {name} not found in registry")
            return None

        with open(cont_path, "r") as f:
            data = yaml.safe_load(f)
            manifest = ServiceManifest(**data)
        
        profile_name = self._resolve_profile_name_for_service(name)

        if profile_name and profile_name in manifest.deployment_profiles:
            profile = manifest.deployment_profiles[profile_name]
            if profile.mode == "external":
                logger.info(f"Service {name} is in external mode (profile: {profile_name}), skipping docker-compose.")
                return None
            
            # If runtime is NOT docker/podman, skip docker-compose generation
            if profile.runtime not in ["docker", "podman"]:
                logger.debug(f"Service {name} runtime is {profile.runtime}, skipping docker-compose.")
                return None

        source = self._resolve_active_source(manifest, name)
        
        if not source:
            return None

        env_file_chain = self._resolve_service_env_file_chain(manifest, source)
        implied_env: Dict[str, str] = {}
        if merged_params:
            for k, v in merged_params.items():
                implied_env[k] = ",".join(map(str, v))

        env, materialized_env_file = self._materialize_service_env(
            name=name,
            env_file_paths=env_file_chain,
            manifest_env=manifest.env,
            source_env=source.env,
            implied_env=implied_env,
        )

        # Backward compatibility for placeholder syntax in environment values
        if merged_params:
            for k, v in merged_params.items():
                placeholder = f"${{HSM_MERGED_PARAMS.{k}}}"
                val_str = ",".join(map(str, v))
                for env_k, env_v in env.items():
                    if isinstance(env_v, str) and placeholder in env_v:
                        env[env_k] = env_v.replace(placeholder, val_str)

        service_cfg = {
            "container_name": source.container_name or manifest.container_name or name,
            "environment": env,
            "ports": list(set(manifest.ports + source.ports)),
            "volumes": list(set(manifest.volumes + source.volumes)),
        }
        if materialized_env_file:
            service_cfg["env_file"] = [materialized_env_file]
        
        if manifest.network_aliases or source.network_aliases:
            service_cfg["networks"] = {
                "default": {
                    "aliases": list(set(manifest.network_aliases + source.network_aliases))
                }
            }

        if source.type == "docker-image":
            service_cfg["image"] = source.image
        elif source.type == "build":
            service_cfg["build"] = {
                "context": str(self.project_root / source.path),
            }
            if source.dockerfile:
                service_cfg["build"]["dockerfile"] = source.dockerfile
        elif source.type == "local": # For containers, local might mean build context
             service_cfg["build"] = {"context": str(self.project_root / source.path)}

        return {name: service_cfg}
