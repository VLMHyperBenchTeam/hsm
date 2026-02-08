import logging
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any, Union
from ..models import LibraryManifest, ServiceManifest, RegistryGroup

logger = logging.getLogger(__name__)

class RegistryManager:
    """Handles CRUD operations and searching in the HSM global registry."""

    def __init__(self, registry_path: Path):
        self.registry_path = registry_path

    def search(self, query: str) -> Dict[str, List[str]]:
        """Search the registry for components."""
        results = {"libraries": [], "services": [], "groups": []}
        query = query.lower()
        
        mapping = {
            "libraries": "libraries",
            "services": "services",
            "library_groups": "groups",
            "service_groups": "groups"
        }
        
        for category, key in mapping.items():
            path = self.registry_path / category
            if path.exists():
                for f in path.glob("*.yaml"):
                    if query in f.stem.lower():
                        results[key].append(f.stem)
        return results

    def add_library(self, name: str, version: str, description: Optional[str] = None,
                    prod_source: Optional[Dict] = None, dev_source: Optional[Dict] = None):
        """Add a library manifest to the registry."""
        libraries_dir = self.registry_path / "libraries"
        libraries_dir.mkdir(parents=True, exist_ok=True)

        manifest_data = {
            "name": name,
            "version": version,
            "description": description,
            "type": "library",
            "sources": {
                "prod": prod_source,
                "dev": dev_source
            }
        }

        manifest_file = libraries_dir / f"{name}.yaml"
        with open(manifest_file, "w") as f:
            yaml.dump(manifest_data, f, sort_keys=False)
        
        logger.info(f"Library '{name}' added to registry at {manifest_file}")

    def add_service(self, name: str, description: Optional[str] = None,
                    prod_source: Optional[Dict] = None, dev_source: Optional[Dict] = None,
                    ports: List[str] = None, volumes: List[str] = None, env: Dict[str, str] = None,
                    container_name: Optional[str] = None, network_aliases: List[str] = None,
                    deployment_profiles: Optional[Dict[str, Any]] = None,
                    dependencies: List[Union[str, Dict]] = None):
        """Add a service manifest to the registry."""
        services_dir = self.registry_path / "services"
        services_dir.mkdir(parents=True, exist_ok=True)

        manifest_data = {
            "name": name,
            "description": description,
            "type": "service",
            "container_name": container_name,
            "network_aliases": network_aliases or [],
            "ports": ports or [],
            "volumes": volumes or [],
            "env": env or {},
            "sources": {
                "prod": prod_source,
                "dev": dev_source
            },
            "dependencies": dependencies or [],
            "deployment_profiles": deployment_profiles or {}
        }

        manifest_file = services_dir / f"{name}.yaml"
        with open(manifest_file, "w") as f:
            yaml.dump(manifest_data, f, sort_keys=False)
        
        logger.info(f"Service '{name}' added to registry at {manifest_file}")

    def add_group(self, name: str, group_type: str, strategy: str, options: List[Union[str, Dict]],
                  description: Optional[str] = None, comment: Optional[str] = None):
        """Add a group manifest to the registry."""
        category = "library_groups" if group_type == "library_group" else "service_groups"
        groups_dir = self.registry_path / category
        groups_dir.mkdir(parents=True, exist_ok=True)

        processed_options = []
        for opt in options:
            if isinstance(opt, str):
                processed_options.append({"name": opt})
            else:
                processed_options.append(opt)

        manifest_data = {
            "name": name,
            "type": group_type,
            "strategy": strategy,
            "options": processed_options,
        }
        if description:
            manifest_data["description"] = description
        if comment:
            manifest_data["comment"] = comment

        manifest_file = groups_dir / f"{name}.yaml"
        with open(manifest_file, "w") as f:
            yaml.dump(manifest_data, f, sort_keys=False)
        
        logger.info(f"Group '{name}' added to registry at {manifest_file}")

    def remove(self, name: str):
        """Remove a component from the registry."""
        found = False
        for category in ["libraries", "services", "library_groups", "service_groups"]:
            path = self.registry_path / category / f"{name}.yaml"
            if path.exists():
                path.unlink()
                logger.info(f"Removed {name} from registry ({category})")
                found = True
        
        if not found:
            raise FileNotFoundError(f"Component '{name}' not found in registry")

    def add_option_to_group(self, group_name: str, option: str):
        """Add an option to a group in the registry."""
        for category in ["library_groups", "service_groups"]:
            path = self.registry_path / category / f"{group_name}.yaml"
            if path.exists():
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                
                options = data.setdefault("options", [])
                if not any(opt.get("name") == option for opt in options):
                    options.append({"name": option})
                    with open(path, "w") as f:
                        yaml.dump(data, f, sort_keys=False)
                    logger.info(f"Added option {option} to group {group_name} in registry")
                return
        raise FileNotFoundError(f"Group {group_name} not found in registry")

    def remove_option_from_group(self, group_name: str, option: str):
        """Remove an option from a group in the registry."""
        for category in ["library_groups", "service_groups"]:
            path = self.registry_path / category / f"{group_name}.yaml"
            if path.exists():
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                
                options = data.get("options", [])
                new_options = [opt for opt in options if opt.get("name") != option]
                if len(new_options) != len(options):
                    data["options"] = new_options
                    with open(path, "w") as f:
                        yaml.dump(data, f, sort_keys=False)
                    logger.info(f"Removed option {option} from group {group_name} in registry")
                return
        raise FileNotFoundError(f"Group {group_name} not found in registry")

    def get_details(self, name: str) -> Optional[Dict[str, Any]]:
        """Get detailed metadata for a component from the registry."""
        for category in ["libraries", "services", "library_groups", "service_groups"]:
            path = self.registry_path / category / f"{name}.yaml"
            if path.exists():
                with open(path, "r") as f:
                    return yaml.safe_load(f)
        return None

    def add_implication(self, component_type: str, name: str, target: str, value: Any):
        """Add an implication to a library or service in the registry."""
        category = "libraries" if component_type == "library" else "services"
        path = self.registry_path / category / f"{name}.yaml"
        
        if not path.exists():
            raise FileNotFoundError(f"{component_type.capitalize()} '{name}' not found in registry")
            
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            
        implies = data.setdefault("implies", {})
        implies[target] = value
        
        with open(path, "w") as f:
            yaml.dump(data, f, sort_keys=False)
        logger.info(f"Added implication {target} to {component_type} {name}")

    def remove_implication(self, component_type: str, name: str, target: str):
        """Remove an implication from a library or service in the registry."""
        category = "libraries" if component_type == "library" else "services"
        path = self.registry_path / category / f"{name}.yaml"
        
        if not path.exists():
            raise FileNotFoundError(f"{component_type.capitalize()} '{name}' not found in registry")
            
        with open(path, "r") as f:
            data = yaml.safe_load(f)
            
        implies = data.get("implies", {})
        if target in implies:
            del implies[target]
            with open(path, "w") as f:
                yaml.dump(data, f, sort_keys=False)
            logger.info(f"Removed implication {target} from {component_type} {name}")

    def add_option_implication(self, group_name: str, option_name: str, target: str, value: Any):
        """Add an implication to a group option in the registry."""
        for category in ["library_groups", "service_groups"]:
            path = self.registry_path / category / f"{group_name}.yaml"
            if path.exists():
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                
                options = data.get("options", [])
                for opt in options:
                    if opt.get("name") == option_name:
                        implies = opt.setdefault("implies", {})
                        implies[target] = value
                        with open(path, "w") as f:
                            yaml.dump(data, f, sort_keys=False)
                        logger.info(f"Added implication {target} to option {option_name} in group {group_name}")
                        return
                raise ValueError(f"Option '{option_name}' not found in group '{group_name}'")
        raise FileNotFoundError(f"Group '{group_name}' not found in registry")

    def remove_option_implication(self, group_name: str, option_name: str, target: str):
        """Remove an implication from a group option in the registry."""
        for category in ["library_groups", "service_groups"]:
            path = self.registry_path / category / f"{group_name}.yaml"
            if path.exists():
                with open(path, "r") as f:
                    data = yaml.safe_load(f)
                
                options = data.get("options", [])
                for opt in options:
                    if opt.get("name") == option_name:
                        implies = opt.get("implies", {})
                        if target in implies:
                            del implies[target]
                            with open(path, "w") as f:
                                yaml.dump(data, f, sort_keys=False)
                            logger.info(f"Removed implication {target} from option {option_name} in group {group_name}")
                        return
                raise ValueError(f"Option '{option_name}' not found in group '{group_name}'")
        raise FileNotFoundError(f"Group '{group_name}' not found in registry")