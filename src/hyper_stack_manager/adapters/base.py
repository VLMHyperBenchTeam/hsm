from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional


class BasePackageManagerAdapter(ABC):
    """Abstract base class for package manager adapters (e.g., uv, pixi, pip)."""

    def __init__(self, project_root: Path):
        """Initialize the adapter.

        Args:
            project_root: Root directory of the project.
        """
        self.project_root = project_root

    @abstractmethod
    def sync(self, packages: List[str], frozen: bool = False):
        """Materialize dependencies into the environment.

        Args:
            packages: List of package requirement strings.
            frozen: If True, do not update dependencies, use lock file.
        """
        pass

    @abstractmethod
    def lock(self):
        """Generate lock file."""
        pass

    @abstractmethod
    def init_lib(self, path: Path):
        """Initialize a new library/package at the given path.

        Args:
            path: Path where to initialize the package.
        """
        pass

    @abstractmethod
    def init_project(self, path: Path):
        """Initialize a new project at the given path.

        Args:
            path: Path where to initialize the project.
        """
        pass

    @abstractmethod
    def init_service(self, path: Path):
        """Initialize a new service at the given path.

        Args:
            path: Path where to initialize the service.
        """
        pass

    @abstractmethod
    def sync_service(self, path: Path, packages: List[str], frozen: bool = False, env_vars: Optional[Dict[str, str]] = None):
        """Sync service dependencies.

        Args:
            path: Path to the service.
            packages: List of package requirement strings to add to the service.
            frozen: If True, do not update dependencies, use lock file.
            env_vars: Optional environment variables to pass to the sync command.
        """
        pass


class BaseContainerAdapter(ABC):
    """Abstract base class for container service adapters (e.g., docker, podman)."""

    def __init__(self, project_root: Path):
        """Initialize the adapter.

        Args:
            project_root: Root directory of the project.
        """
        self.project_root = project_root

    @abstractmethod
    def generate_config(self, services: List[Dict[str, Any]]):
        """Generate orchestration configuration (e.g., docker-compose.yml).

        Args:
            services: List of service configurations.
        """
        pass

    @abstractmethod
    def up(self, services: Optional[List[str]] = None):
        """Start services.

        Args:
            services: Optional list of service names to start.
        """
        pass

    @abstractmethod
    def down(self):
        """Stop and remove services."""
        pass