import pytest
import yaml
import shutil
import subprocess
from pathlib import Path
from hyper_stack_manager.cli.root import app


ASSETS_ENV_DIR = Path(__file__).parent / "assets" / "env_files"


def _copy_env_asset(hsm_sandbox: Path, filename: str, target_name: str | None = None) -> str:
    """Copy env asset into sandbox and return relative file name."""
    src = ASSETS_ENV_DIR / filename
    dst_name = target_name or filename
    dst = hsm_sandbox / dst_name
    shutil.copy2(src, dst)
    return dst_name


def _create_fake_git_repo(path: Path, name: str) -> str:
    """Create minimal local git repo for offline tests."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=path, check=True)
    (path / "pyproject.toml").write_text(
        f'[project]\nname = "{name}"\nversion = "0.1.0"\ndependencies = []',
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=path, check=True)
    return f"file://{path.absolute()}"

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
    _copy_env_asset(hsm_sandbox, "invalid.env")

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
    _copy_env_asset(hsm_sandbox, "service_conflict.env", "service.env")

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

def test_env_fail_conflict_source_env(runner, hsm_sandbox):
    """ENV-FAIL-004: sync fails if key exists in env_file and source.env."""
    _copy_env_asset(hsm_sandbox, "source_conflict.env")

    runner.invoke(app, [
        "registry", "service", "add", "fail-service",
        "--runtime", "uv",
        "--build-path", "services/fail-service",
        "--env-file", "source_conflict.env",
        "--no-input"
    ])

    svc_path = hsm_sandbox / "hsm-registry" / "services" / "fail-service.yaml"
    with open(svc_path, "r") as f:
        data = yaml.safe_load(f)
    data["sources"]["dev"]["env"] = {"CONFLICT_KEY": "value_from_source"}
    with open(svc_path, "w") as f:
        yaml.dump(data, f)

    runner.invoke(app, ["init"])
    runner.invoke(app, ["service", "add", "fail-service"])
    runner.invoke(app, ["service", "mode", "fail-service", "dev"])

    result = runner.invoke(app, ["sync"])

    assert result.exit_code != 0
    assert "CONFLICT_KEY" in result.stdout
    assert "conflict" in result.stdout.lower()

def test_env_fail_conflict_implies(runner, hsm_sandbox):
    """ENV-FAIL-005: sync fails if key exists in env_file and implies params."""
    _copy_env_asset(hsm_sandbox, "implies_conflict.env")

    local_repo = _create_fake_git_repo(hsm_sandbox.parent / "imply_repo", "imply-lib")

    runner.invoke(app, [
        "registry", "library", "add", "imply-lib",
        "--version", "0.1.0",
        "--prod-type", "git",
        "--prod-url", local_repo,
        "--no-input"
    ])
    runner.invoke(app, [
        "registry", "library", "implies", "add", "imply-lib",
        "service:fail-service", "DB_NAME=implied_db"
    ])

    runner.invoke(app, [
        "registry", "service", "add", "fail-service",
        "--image", "nginx:latest",
        "--runtime", "docker",
        "--env-file", "implies_conflict.env",
        "--no-input"
    ])

    runner.invoke(app, ["init"])
    runner.invoke(app, ["library", "add", "imply-lib"])

    result = runner.invoke(app, ["sync", "--no-verify"])

    assert result.exit_code != 0
    assert "DB_NAME" in result.stdout
    assert "conflict" in result.stdout.lower()

def test_env_fail_conflict_manifest_source_implies(runner, hsm_sandbox):
    """ENV-FAIL-006: sync fails on duplicates across manifest.env/source.env/implies."""
    local_repo = _create_fake_git_repo(hsm_sandbox.parent / "imply_repo_chain", "imply-lib")

    runner.invoke(app, [
        "registry", "library", "add", "imply-lib",
        "--version", "0.1.0",
        "--prod-type", "git",
        "--prod-url", local_repo,
        "--no-input"
    ])
    runner.invoke(app, [
        "registry", "library", "implies", "add", "imply-lib",
        "service:fail-service", "CHAIN_KEY=from_implies"
    ])

    runner.invoke(app, [
        "registry", "service", "add", "fail-service",
        "--runtime", "uv",
        "--build-path", "services/fail-service",
        "--env", "CHAIN_KEY=from_manifest",
        "--no-input"
    ])

    svc_path = hsm_sandbox / "hsm-registry" / "services" / "fail-service.yaml"
    with open(svc_path, "r") as f:
        data = yaml.safe_load(f)
    data["sources"]["dev"]["env"] = {"CHAIN_KEY": "from_source"}
    with open(svc_path, "w") as f:
        yaml.dump(data, f)

    runner.invoke(app, ["init"])
    runner.invoke(app, ["library", "add", "imply-lib"])
    runner.invoke(app, ["service", "add", "fail-service"])
    runner.invoke(app, ["service", "mode", "fail-service", "dev"])

    result = runner.invoke(app, ["sync"])

    assert result.exit_code != 0
    assert "CHAIN_KEY" in result.stdout
    assert "conflict" in result.stdout.lower()
