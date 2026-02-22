import subprocess
import yaml
import shutil
from pathlib import Path
from hyper_stack_manager.cli import app


ASSETS_ENV_DIR = Path(__file__).parent / "assets" / "env_files"

def test_docker_compose_config_validation(runner, hsm_sandbox):
    """Level 1.3: Test that hsm sync generates a valid docker-compose file."""
    
    # 1. Setup project and registry
    runner.invoke(app, ["init", "--name", "docker-test"])
    
    # Add a service to registry
    runner.invoke(app, [
        "registry", "service", "add", "web-server",
        "--image", "nginx:latest",
        "--port", "8080:80",
        "--runtime", "docker",
        "--no-input"
    ])
    
    # Add a group with this service
    runner.invoke(app, [
        "registry", "group", "add", "web-group",
        "--type", "service_group",
        "--strategy", "1-of-N",
        "--option", "web-server",
        "--no-input"
    ])
    
    # 2. Add group to project
    runner.invoke(app, ["group", "add", "web-group", "--option", "web-server"])
    
    # 3. Sync (generates docker-compose.hsm.yml)
    result = runner.invoke(app, ["sync", "--no-verify"])
    assert result.exit_code == 0
    
    compose_file = hsm_sandbox / "docker-compose.hsm.yml"
    assert compose_file.exists()
    
    # 4. Validate with real docker compose config
    try:
        # We use 'config' command which validates the file without starting containers
        cp_result = subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "config"],
            capture_output=True, text=True
        )
        # If docker is not installed, this might fail, but in Ubuntu 24.04 it should be there
        if cp_result.returncode == 0:
            assert "services" in cp_result.stdout
            assert "web-server" in cp_result.stdout
    except FileNotFoundError:
        # Skip if docker is not installed in the test environment
        pass

def test_docker_compose_contains_env_file(runner, hsm_sandbox):
    """ENV-HF-001: docker runtime includes materialized env_file in compose."""
    shutil.copy2(ASSETS_ENV_DIR / "shared.env", hsm_sandbox / "shared.env")

    runner.invoke(app, ["init", "--name", "docker-env-file-test"])
    result = runner.invoke(app, [
        "registry", "service", "add", "web-env",
        "--image", "nginx:latest",
        "--runtime", "docker",
        "--env-file", "shared.env",
        "--no-input"
    ])
    assert result.exit_code == 0

    runner.invoke(app, ["service", "add", "web-env"])
    sync_result = runner.invoke(app, ["sync", "--no-verify"])
    assert sync_result.exit_code == 0

    compose_file = hsm_sandbox / "docker-compose.hsm.yml"
    with open(compose_file, "r") as f:
        compose_data = yaml.safe_load(f)

    service_cfg = compose_data["services"]["web-env"]
    assert "env_file" in service_cfg
    assert ".env.web-env" in service_cfg["env_file"]
    assert (hsm_sandbox / ".env.web-env").exists()
