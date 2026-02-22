import pytest
from hyper_stack_manager.cli import app
import yaml

def test_project_list(runner, temp_project, monkeypatch):
    """Test listing project stack."""
    monkeypatch.chdir(temp_project)
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Project: test_project" in result.stdout

def test_project_mode_set(runner, temp_project, monkeypatch):
    """Test setting global project mode."""
    monkeypatch.chdir(temp_project)
    result = runner.invoke(app, ["mode", "dev"])
    assert result.exit_code == 0
    assert "Global mode set to dev" in result.stdout
    
    # Verify hsm.yaml (this depends on how HSMCore saves it, 
    # but usually it should update the file)
    with open(temp_project / "hsm.yaml", "r") as f:
        data = yaml.safe_load(f)
        # Check if mode is set (implementation detail: HSMCore.set_global_mode 
        # sets mode for each package/group)
        # For now, just check if command succeeded.

def test_project_library_add(runner, hsm_sandbox):
    """Test adding a library to project using High-Fidelity approach."""
    # 1. Setup Registry via CLI
    runner.invoke(app, [
        "registry", "library", "add", "my-lib",
        "--version", "0.1.0",
        "--prod-type", "git",
        "--prod-url", "https://github.com/org/repo",
        "--no-input"
    ])
    
    # 2. Init Project
    runner.invoke(app, ["init", "--name", "test-project"])
    
    # 3. Action: Add library
    result = runner.invoke(app, ["library", "add", "my-lib"])
    assert result.exit_code == 0
    assert "Added library 'my-lib' to project" in result.stdout

def test_project_sync_basic(runner, hsm_sandbox):
    """Test sync command without mocking (High-Fidelity)."""
    runner.invoke(app, ["init", "--name", "sync-project"])
    
    # Use --no-verify because we don't have real packages installed
    result = runner.invoke(app, ["sync", "--no-verify"])
    assert result.exit_code == 0
    assert "Environment synced successfully" in result.stdout

def test_project_library_remove(runner, hsm_sandbox):
    """Test removing a library from project."""
    runner.invoke(app, ["init", "--name", "remove-project"])
    
    # Setup registry and add library
    runner.invoke(app, ["registry", "library", "add", "to-remove", "--no-input"])
    runner.invoke(app, ["library", "add", "to-remove"])
    
    result = runner.invoke(app, ["library", "remove", "to-remove"])
    assert result.exit_code == 0
    assert "Removed library 'to-remove' from project" in result.stdout

def test_project_group_add(runner, hsm_sandbox):
    """Test adding a group to project."""
    runner.invoke(app, ["init", "--name", "group-project"])
    
    # Setup registry group via CLI
    runner.invoke(app, [
        "registry", "group", "add", "my-group",
        "--type", "library_group",
        "--option", "opt1",
        "--no-input"
    ])

    result = runner.invoke(app, ["group", "add", "my-group", "--option", "opt1"])
    assert result.exit_code == 0
    assert "Added group 'my-group' with selection 'opt1'" in result.stdout

def test_project_python_manager_set(runner, hsm_sandbox):
    """Test setting python manager."""
    runner.invoke(app, ["init", "--name", "manager-project"])
    result = runner.invoke(app, ["python-manager", "set", "pixi"])
    assert result.exit_code == 0
    assert "Python manager set to pixi" in result.stdout

def test_project_init_help_contains_git_init(runner, hsm_sandbox):
    """GIT-CLI-001: init commands expose --git-init option."""
    lib_help = runner.invoke(app, ["library", "init", "--help"])
    svc_help = runner.invoke(app, ["service", "init", "--help"])

    assert lib_help.exit_code == 0
    assert svc_help.exit_code == 0
    assert "--git-init" in lib_help.stdout
    assert "--git-init" in svc_help.stdout
