import pytest
import os
import shutil
from pathlib import Path
from typer.testing import CliRunner
from dotenv import load_dotenv

# Load .env file if it exists in the project root
load_dotenv()

# Configuration for debugging
HSM_KEEP_RUNS = int(os.getenv("HSM_KEEP_RUNS", "10"))

@pytest.fixture
def runner():
    """Fixture for Typer CliRunner."""
    return CliRunner()

def get_versioned_path(base_path: Path) -> Path:
    """Get the next versioned path (run_N) and update LATEST.txt."""
    base_path.mkdir(parents=True, exist_ok=True)
    latest_file = base_path / "LATEST.txt"
    
    current_run = 0
    if latest_file.exists():
        try:
            current_run = int(latest_file.read_text().strip())
        except ValueError:
            current_run = 0
            
    next_run = current_run + 1
    run_path = base_path / f"run_{next_run}"
    
    # Cleanup old runs
    old_run_to_delete = base_path / f"run_{next_run - HSM_KEEP_RUNS}"
    if old_run_to_delete.exists():
        shutil.rmtree(old_run_to_delete)
        
    run_path.mkdir(parents=True, exist_ok=True)
    latest_file.write_text(str(next_run))
    return run_path

@pytest.fixture
def hsm_sandbox(tmp_path, monkeypatch, request):
    """Fixture to create a temporary HSM sandbox with isolated registry.
    
    If HSM_DEBUG_TESTS=1, uses versioned directories in debug_tests/.
    Otherwise, uses standard tmp_path.
    """
    if os.getenv("HSM_DEBUG_TESTS") == "1":
        project_root = Path(__file__).parent.parent
        test_name = request.node.name.replace("[", "_").replace("]", "_")
        base_debug_path = project_root / "debug_tests" / test_name
        sandbox_dir = get_versioned_path(base_debug_path)
    else:
        sandbox_dir = tmp_path / "hsm_sandbox"
        sandbox_dir.mkdir(parents=True, exist_ok=True)
    
    registry_dir = sandbox_dir / "hsm-registry"
    registry_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure registry structure for VES
    for sub_dir in ["libraries", "services", "library_groups", "service_groups"]:
        (registry_dir / sub_dir).mkdir(parents=True, exist_ok=True)
    
    # Set environment variable for isolated registry
    monkeypatch.setenv("HSM_REGISTRY_PATH", str(registry_dir))
    
    # Change directory to sandbox
    monkeypatch.chdir(sandbox_dir)
    
    return sandbox_dir

@pytest.fixture
def temp_project(tmp_path):
    """Fixture to create a temporary HSM project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    
    # Create a basic hsm.yaml
    hsm_yaml = project_dir / "hsm.yaml"
    hsm_yaml.write_text("""
project:
  name: test_project
  manager: uv
""")
    
    return project_dir