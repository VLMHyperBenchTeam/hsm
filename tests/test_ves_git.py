import os
import pytest
import yaml
import subprocess
import shutil
from pathlib import Path
from hyper_stack_manager.cli.root import app

def test_service_git_materialization(runner, hsm_sandbox):
    """Test that HSM can clone a service from a local Git repository using CLI."""
    project_root = hsm_sandbox
    
    # 1. Setup a "remote" Git repository
    remote_dir = project_root.parent / "fake_remote"
    if remote_dir.exists():
        shutil.rmtree(remote_dir)
    remote_dir.mkdir()
    
    # Initialize git and create a project
    subprocess.run(["git", "init"], cwd=remote_dir, check=True)
    (remote_dir / "pyproject.toml").write_text('[project]\nname = "git-service"\nversion = "0.1.0"\ndependencies = []')
    (remote_dir / "README.md").write_text("# Git Service")
    
    subprocess.run(["git", "add", "."], cwd=remote_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=remote_dir, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=remote_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=remote_dir, check=True)
    
    # 2. Register this service in HSM registry using CLI
    remote_url = f"file://{remote_dir.absolute()}"
    
    runner.invoke(app, ["init"])
    
    # Use registry command to add service
    result = runner.invoke(app, [
        "registry", "service", "add", "git-service",
        "--description", "Git Test Service",
        "--build-path", "services/git-service", # dev path
        "--runtime", "uv",
        "--no-input"
    ])
    assert result.exit_code == 0
    
    # Manually patch the registry file to set prod source to git (CLI might not support it yet)
    # TODO: Add --prod-url and --prod-type to registry service add
    registry_file = project_root / "hsm-registry" / "services" / "git-service.yaml"
    with open(registry_file, "r") as f:
        data = yaml.safe_load(f)
    
    data["sources"]["prod"] = {"type": "git", "url": remote_url}
    with open(registry_file, "w") as f:
        yaml.dump(data, f)
        
    # 3. Add service to project and sync
    runner.invoke(app, ["service", "add", "git-service"])
    # Set mode to prod to trigger git clone
    runner.invoke(app, ["service", "mode", "git-service", "prod"])
    
    result = runner.invoke(app, ["sync"])
    assert result.exit_code == 0
    
    # 4. Verify materialization
    service_dir = project_root / "services" / "git-service"
    if not service_dir.exists():
        print(f"DEBUG: Service dir {service_dir} does not exist!")
        print(f"DEBUG: Project root contents: {list(project_root.iterdir())}")
        if (project_root / "services").exists():
             print(f"DEBUG: Services dir contents: {list((project_root / 'services').iterdir())}")

    assert service_dir.exists()
    assert (service_dir / "pyproject.toml").exists()
    assert (service_dir / "README.md").read_text() == "# Git Service"
    assert (service_dir / ".git").exists(), "Should be a git clone"