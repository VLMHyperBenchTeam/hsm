import pytest
import yaml
from hyper_stack_manager.cli.root import app

def test_env_fail_missing_file(runner, hsm_sandbox):
    """ENV-FAIL-001: sync fails if env_file is missing."""
    # 1. Setup Registry with a non-existent env_file
    runner.invoke(app, [
        "registry", "service", "add", "fail-service",
        "--runtime", "uv",
        "--no-input"
    ])
    
    # Manually add env_file to registry manifest (CLI support pending)
    svc_path = hsm_sandbox / "hsm-registry" / "services" / "fail-service.yaml"
    with open(svc_path, "r") as f:
        data = yaml.safe_load(f)
    
    # We'll assume the new structure supports env_file at service level
    data["env_file"] = "missing.env"
    with open(svc_path, "w") as f:
        yaml.dump(data, f)

    # 2. Setup Project
    runner.invoke(app, ["init"])
    runner.invoke(app, ["service", "add", "fail-service"])

    # 3. Action: Sync
    result = runner.invoke(app, ["sync"])
    
    # 4. Verify: Should fail with clear message
    assert result.exit_code != 0
    assert "missing.env" in result.stdout
    assert "not found" in result.stdout.lower()

def test_env_fail_invalid_format(runner, hsm_sandbox):
    """ENV-FAIL-002: sync fails if env_file has invalid format."""
    # 1. Create invalid env file
    env_file = hsm_sandbox / "invalid.env"
    env_file.write_text("INVALID_LINE_WITHOUT_EQUALS")

    # 2. Setup Registry
    runner.invoke(app, [
        "registry", "service", "add", "fail-service",
        "--runtime", "uv",
        "--no-input"
    ])
    
    svc_path = hsm_sandbox / "hsm-registry" / "services" / "fail-service.yaml"
    with open(svc_path, "r") as f:
        data = yaml.safe_load(f)
    data["env_file"] = "invalid.env"
    with open(svc_path, "w") as f:
        yaml.dump(data, f)

    # 3. Setup Project
    runner.invoke(app, ["init"])
    runner.invoke(app, ["service", "add", "fail-service"])

    # 4. Action: Sync
    result = runner.invoke(app, ["sync"])
    
    # 5. Verify
    assert result.exit_code != 0
    assert "INVALID_LINE_WITHOUT_EQUALS" in result.stdout
    assert "format" in result.stdout.lower()

def test_env_fail_conflict_manifest(runner, hsm_sandbox):
    """ENV-FAIL-003: sync fails if key exists in both env_file and manifest.env."""
    # 1. Create env file
    env_file = hsm_sandbox / "service.env"
    env_file.write_text("CONFLICT_KEY=value1")

    # 2. Setup Registry
    runner.invoke(app, [
        "registry", "service", "add", "fail-service",
        "--runtime", "uv",
        "--env", "CONFLICT_KEY=value2",
        "--no-input"
    ])
    
    svc_path = hsm_sandbox / "hsm-registry" / "services" / "fail-service.yaml"
    with open(svc_path, "r") as f:
        data = yaml.safe_load(f)
    data["env_file"] = "service.env"
    with open(svc_path, "w") as f:
        yaml.dump(data, f)

    # 3. Setup Project
    runner.invoke(app, ["init"])
    runner.invoke(app, ["service", "add", "fail-service"])

    # 4. Action: Sync
    result = runner.invoke(app, ["sync"])
    
    # 5. Verify
    assert result.exit_code != 0
    assert "CONFLICT_KEY" in result.stdout
    assert "conflict" in result.stdout.lower()
