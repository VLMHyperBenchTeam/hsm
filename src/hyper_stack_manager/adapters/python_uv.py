import subprocess
import logging
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import tomlkit
from .base import BasePackageManagerAdapter

logger = logging.getLogger(__name__)

class UvAdapter(BasePackageManagerAdapter):
    """Adapter for the uv package manager."""

    def __init__(self, project_root: Path):
        super().__init__(project_root)
        self.pyproject_path = project_root / "pyproject.toml"

    def _load_env_file(self, env_file: Path) -> Dict[str, str]:
        """Load KEY=VALUE pairs from .env file with strict validation."""
        if not env_file.exists():
            raise FileNotFoundError(f"env_file not found: {env_file}")

        result: Dict[str, str] = {}
        with env_file.open("r", encoding="utf-8") as f:
            for idx, raw_line in enumerate(f, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(
                        f"Invalid env file format at {env_file}:{idx}: '{line}'"
                    )
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if not key:
                    raise ValueError(
                        f"Invalid env file format at {env_file}:{idx}: empty key"
                    )
                result[key] = value

        return result

    def _get_base_cmd(self) -> List[str]:
        """Get the base uv command with optional --system flag."""
        if os.getenv("HSM_USE_SYSTEM") == "1":
            return ["uv", "--system"]
        return ["uv"]

    def sync(self, packages: List[str], frozen: bool = False):
        """Sync dependencies using uv."""
        logger.info(f"Syncing {len(packages)} packages with uv...")
        
        # 1. Update pyproject.toml dependencies
        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at {self.pyproject_path}. Run 'hsm init' first.")

        with open(self.pyproject_path, "r") as f:
            config = tomlkit.parse(f.read())
        
        # Ensure project section exists
        project = config.setdefault("project", tomlkit.table())
        project["dependencies"] = packages
        
        with open(self.pyproject_path, "w") as f:
            f.write(tomlkit.dumps(config))

        # 2. Run uv sync
        cmd = self._get_base_cmd() + ["sync"]
        if frozen:
            cmd.append("--frozen")
        
        try:
            subprocess.run(cmd, check=True, cwd=self.project_root)
        except subprocess.CalledProcessError as e:
            logger.error(f"uv sync failed: {e}")
            raise

    def lock(self):
        """Generate uv.lock file."""
        cmd = self._get_base_cmd() + ["lock"]
        try:
            subprocess.run(cmd, check=True, cwd=self.project_root)
        except subprocess.CalledProcessError as e:
            logger.error(f"uv lock failed: {e}")
            raise

    def init_lib(self, path: Path):
        """Initialize a new library with uv init --lib --no-workspace."""
        path.mkdir(parents=True, exist_ok=True)
        cmd = self._get_base_cmd() + ["init", "--lib", "--no-workspace"]
        try:
            subprocess.run(cmd, check=True, cwd=path)
        except subprocess.CalledProcessError as e:
            logger.error(f"uv init failed: {e}")
            raise

    def init_project(self, path: Path):
        """Initialize a new project with uv init --no-workspace."""
        path.mkdir(parents=True, exist_ok=True)
        cmd = self._get_base_cmd() + ["init", "--no-workspace"]
        try:
            subprocess.run(cmd, check=True, cwd=path)
        except subprocess.CalledProcessError as e:
            logger.error(f"uv init failed: {e}")
            raise

    def init_service(self, path: Path):
        """Initialize a new service with uv init --no-workspace."""
        path.mkdir(parents=True, exist_ok=True)
        cmd = self._get_base_cmd() + ["init", "--no-workspace"]
        try:
            subprocess.run(cmd, check=True, cwd=path)
        except subprocess.CalledProcessError as e:
            logger.error(f"uv init (service) failed: {e}")
            raise

    def sync_service(
        self,
        path: Path,
        packages: List[str],
        frozen: bool = False,
        env_vars: Optional[Dict[str, str]] = None,
        env_file: Optional[str] = None,
    ):
        """Sync service dependencies using uv sync inside the service path."""
        env = os.environ.copy()
        env["UV_NO_WORKSPACE"] = "1"
        # Ensure we don't use the parent venv
        env.pop("VIRTUAL_ENV", None)

        if env_file:
            env_path = Path(env_file)
            if not env_path.is_absolute():
                env_path = (self.project_root / env_path).resolve()
            env.update(self._load_env_file(env_path))

        if env_vars:
            env.update(env_vars)

        # 1. Add dependencies if any
        if packages:
            logger.info(f"Adding {len(packages)} dependencies to service at {path}...")
            add_cmd = self._get_base_cmd() + ["add", "--no-workspace"] + packages
            try:
                subprocess.run(add_cmd, check=True, cwd=path, env=env)
            except subprocess.CalledProcessError as e:
                logger.error(f"uv add (service) failed: {e}")
                raise

        # 2. Run uv sync
        cmd = self._get_base_cmd() + ["sync"]
        if frozen:
            cmd.append("--frozen")
        
        try:
            subprocess.run(cmd, check=True, cwd=path, env=env)
        except subprocess.CalledProcessError as e:
            logger.error(f"uv sync (service) failed: {e}")
            raise
