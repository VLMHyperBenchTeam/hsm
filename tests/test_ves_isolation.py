import os
import pytest
import yaml
from pathlib import Path
from hyper_stack_manager.cli.root import app

def test_service_init_isolation(runner, hsm_sandbox):
    """Test that 'hsm service init' creates an isolated project not linked to the parent workspace."""
    project_root = hsm_sandbox
    
    # 1. Initialize main project
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0
        
    root_pyproject = project_root / "pyproject.toml"
    assert root_pyproject.exists()
    
    # 2. Create a service
    result = runner.invoke(app, ["service", "init", "my-service", "--runtime", "uv"])
    assert result.exit_code == 0
    
    # 3. CHECK 1: Root pyproject.toml must NOT contain the service in workspace members
    content = root_pyproject.read_text()
    # uv init might add members if not careful, we want to ensure it didn't
    assert "my-service" not in content, "Service was automatically added to workspace members in root pyproject.toml!"
    
    # 4. CHECK 2: Service directory must be autonomous
    service_dir = project_root / "services" / "my-service"
    assert service_dir.exists()
    assert (service_dir / "pyproject.toml").exists()
    
    # 5. CHECK 3: Registry entry must have correct runtime
    registry_file = project_root / "hsm-registry" / "services" / "my-service.yaml"
    assert registry_file.exists()
    with open(registry_file, "r") as f:
        registry_data = yaml.safe_load(f)
        assert registry_data["deployment_profiles"]["default"]["runtime"] == "uv"

def test_service_sync_isolation(runner, hsm_sandbox):
    """Test that 'hsm sync' for a uv service creates a local .venv and uv.lock."""
    project_root = hsm_sandbox
    
    # Initialize project and service
    runner.invoke(app, ["init"])
    runner.invoke(app, ["service", "init", "my-service", "--runtime", "uv"])
    
    # Add service to hsm.yaml
    runner.invoke(app, ["service", "add", "my-service"])
    
    # Run sync
    # Note: This actually calls 'uv sync' with UV_NO_WORKSPACE=1
    result = runner.invoke(app, ["sync"])
    assert result.exit_code == 0
    
    service_dir = project_root / "services" / "my-service"
    
    # If uv sync was successful, these should exist inside the service dir
    # and NOT just in the root.
    assert (service_dir / "uv.lock").exists(), "Service should have its own uv.lock"
    # .venv might be created depending on how uv is configured,
    # but uv.lock is a definitive sign of a standalone project.