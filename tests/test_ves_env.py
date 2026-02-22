import os
import pytest
import yaml
import shutil
import subprocess
from pathlib import Path
from hyper_stack_manager.cli.root import app


ASSETS_ENV_DIR = Path(__file__).parent / "assets" / "env_files"

def test_service_env_and_deps_propagation(runner, hsm_sandbox):
    """
    High-Fidelity test for ENV and Dependency propagation using a "Canary" package.
    The canary package uses Hatchling and fails to build if HSM_CANARY_VAR is missing.
    """
    project_root = hsm_sandbox
    
    # 1. Setup the "Canary" package from assets
    assets_dir = Path(__file__).parent / "assets" / "canary_pkg"
    canary_dir = project_root.parent / "canary_pkg"
    if canary_dir.exists():
        shutil.rmtree(canary_dir)
    shutil.copytree(assets_dir, canary_dir)
    
    # 2. Setup HSM project and registry using CLI
    runner.invoke(app, ["init"])
    
    # Register the canary package as a library
    result = runner.invoke(app, [
        "registry", "library", "add", "canary-pkg",
        "--version", "0.1.0",
        "--prod-type", "local",
        "--dev-path", str(canary_dir.absolute()),
        "--no-input"
    ])
    assert result.exit_code == 0

    # Register a service that depends on the canary and has the ENV var
    result = runner.invoke(app, [
        "registry", "service", "add", "env-service",
        "--description", "Test ENV Service",
        "--env", "HSM_CANARY_VAR=FLYING",
        "--build-path", "services/env-service",
        "--runtime", "uv",
        "--dependency", "canary-pkg",
        "--no-input"
    ])
    assert result.exit_code == 0

    # 3. Initialize the service directory
    runner.invoke(app, ["service", "init", "env-service"])
    
    # 4. Add service to project and sync
    runner.invoke(app, ["service", "add", "env-service"])
    # Set mode to dev since we only provided dev-path (build-path)
    runner.invoke(app, ["service", "mode", "env-service", "dev"])
    
    # Action: Sync
    # This will:
    # 1. Collect 'canary-pkg' as dependency for 'env-service'
    # 2. Call 'uv add canary-pkg' inside services/env-service
    # 3. Call 'uv sync' with HSM_CANARY_VAR=FLYING
    # 4. Hatchling will check the ENV var during build
    result = runner.invoke(app, ["sync"])
    
    # 5. Verify
    assert result.exit_code == 0, f"Sync failed! Output: {result.stdout}"
    assert (project_root / "services" / "env-service" / "uv.lock").exists()
    
    # Verify that canary-pkg is actually installed in the service's venv
    # CRITICAL: We must clear VIRTUAL_ENV to ensure uv uses the local .venv of the service
    test_env = os.environ.copy()
    test_env.pop("VIRTUAL_ENV", None)
    test_env["UV_NO_WORKSPACE"] = "1"
    
    list_result = subprocess.run(
        ["uv", "pip", "list", "--python", ".venv/bin/python"],
        cwd=project_root / "services" / "env-service",
        capture_output=True, text=True, check=True,
        env=test_env
    )
    # Check for package name (case-insensitive and handling dashes/underscores)
    output = list_result.stdout.lower().replace("-", "_")
    assert "canary_pkg" in output or "canary-pkg" in list_result.stdout.lower()

def test_service_env_file_and_deps_propagation(runner, hsm_sandbox):
    """ENV-HF-002: uv service receives env from env_file during sync."""
    project_root = hsm_sandbox

    assets_dir = Path(__file__).parent / "assets" / "canary_pkg"
    canary_dir = project_root.parent / "canary_pkg_env_file"
    if canary_dir.exists():
        shutil.rmtree(canary_dir)
    shutil.copytree(assets_dir, canary_dir)

    runner.invoke(app, ["init"])

    lib_result = runner.invoke(app, [
        "registry", "library", "add", "canary-pkg",
        "--version", "0.1.0",
        "--prod-type", "local",
        "--dev-path", str(canary_dir.absolute()),
        "--no-input"
    ])
    assert lib_result.exit_code == 0

    shutil.copy2(ASSETS_ENV_DIR / "canary.env", project_root / "svc.env")

    svc_result = runner.invoke(app, [
        "registry", "service", "add", "env-file-service",
        "--description", "Test ENV File Service",
        "--build-path", "services/env-file-service",
        "--runtime", "uv",
        "--dependency", "canary-pkg",
        "--env-file", "svc.env",
        "--no-input"
    ])
    assert svc_result.exit_code == 0

    runner.invoke(app, ["service", "init", "env-file-service"])
    runner.invoke(app, ["service", "add", "env-file-service"])
    runner.invoke(app, ["service", "mode", "env-file-service", "dev"])

    sync_result = runner.invoke(app, ["sync"])
    assert sync_result.exit_code == 0, f"Sync failed! Output: {sync_result.stdout}"

    assert (project_root / "services" / "env-file-service" / "uv.lock").exists()
    assert (project_root / ".env.env-file-service").exists()

    test_env = os.environ.copy()
    test_env.pop("VIRTUAL_ENV", None)
    test_env["UV_NO_WORKSPACE"] = "1"

    list_result = subprocess.run(
        ["uv", "pip", "list", "--python", ".venv/bin/python"],
        cwd=project_root / "services" / "env-file-service",
        capture_output=True,
        text=True,
        check=True,
        env=test_env,
    )

    output = list_result.stdout.lower().replace("-", "_")
    assert "canary_pkg" in output or "canary-pkg" in list_result.stdout.lower()
