import pytest
from hyper_stack_manager.cli.root import app

def test_manual_sandbox(runner, hsm_sandbox):
    """
    Special 'test' to initialize a manual sandbox for debugging.
    Run with: HSM_DEBUG_TESTS=1 uv run pytest tests/test_sandbox.py
    """
    # Initialize the project using HSM CLI
    result = runner.invoke(app, ["init", "--name", "manual-sandbox"])
    assert result.exit_code == 0
    
    print(f"\n\n[MANUAL SANDBOX READY]")
    print(f"Path: {hsm_sandbox}")
    print(f"Registry: {hsm_sandbox}/hsm-registry")
    print(f"You can now 'cd {hsm_sandbox}' and run hsm commands manually.\n")