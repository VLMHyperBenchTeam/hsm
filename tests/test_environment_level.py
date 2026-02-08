import os
import yaml
import pytest
import subprocess
import shutil
from pathlib import Path
from hyper_stack_manager.cli import app

def create_fake_git_repo(path: Path, name: str):
    """Helper to create a minimal local git repository."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    subprocess.run(["git", "init"], cwd=path, check=True)
    (path / "pyproject.toml").write_text(f'[project]\nname = "{name}"\nversion = "0.1.0"\ndependencies = []')
    subprocess.run(["git", "add", "."], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=path, check=True)
    return f"file://{path.absolute()}"

def test_case_1_implication_merging(runner, hsm_sandbox):
    """Case 1: Shared Service (Implication Merging).
    Two libraries imply the same service with different params.
    """
    # 1. Setup Registry
    # Service: postgres
    runner.invoke(app, [
        "registry", "service", "add", "postgres",
        "--image", "postgres:16-alpine",
        "--env", "POSTGRES_MULTIPLE_DATABASES=${HSM_MERGED_PARAMS.db_name}",
        "--no-input"
    ])
    
    # Create local git repos for libraries to avoid network calls
    auth_repo = create_fake_git_repo(hsm_sandbox.parent / "auth_repo", "auth-service")
    billing_repo = create_fake_git_repo(hsm_sandbox.parent / "billing_repo", "billing-service")

    # Library: auth-service
    runner.invoke(app, [
        "registry", "library", "add", "auth-service",
        "--version", "1.0.0",
        "--prod-type", "git",
        "--prod-url", auth_repo,
        "--no-input"
    ])
    # Add implication via CLI
    runner.invoke(app, [
        "registry", "library", "implies", "add", "auth-service",
        "service:postgres", "db_name=auth_db"
    ])

    # Library: billing-service
    runner.invoke(app, [
        "registry", "library", "add", "billing-service",
        "--version", "1.0.0",
        "--prod-type", "git",
        "--prod-url", billing_repo,
        "--no-input"
    ])
    # Add implication via CLI
    runner.invoke(app, [
        "registry", "library", "implies", "add", "billing-service",
        "service:postgres", "db_name=billing_db"
    ])

    # 2. Setup Project
    runner.invoke(app, ["init", "--name", "shared-service-project"])
    runner.invoke(app, ["library", "add", "auth-service"])
    runner.invoke(app, ["library", "add", "billing-service"])

    # 3. Sync
    # Используем --no-verify, так как в песочнице мы проверяем логику резолвинга, а не реальное состояние системы
    result = runner.invoke(app, ["sync", "--no-verify"])
    assert result.exit_code == 0

    # 4. Validate docker-compose.hsm.yml
    compose_path = hsm_sandbox / "docker-compose.hsm.yml"
    assert compose_path.exists()
    with open(compose_path, "r") as f:
        compose_data = yaml.safe_load(f)
    
    postgres_svc = compose_data["services"]["postgres"]
    env = postgres_svc["environment"]
    # HSM_MERGED_PARAMS.db_name should be "auth_db,billing_db" or "billing_db,auth_db"
    assert "auth_db" in env["POSTGRES_MULTIPLE_DATABASES"]
    assert "billing_db" in env["POSTGRES_MULTIPLE_DATABASES"]
    assert "," in env["POSTGRES_MULTIPLE_DATABASES"]

def test_case_2_hybrid_cloud(runner, hsm_sandbox):
    """Case 2: Hybrid Cloud (Managed + External).
    One service is managed (docker), another is external (remote host).
    """
    # 1. Setup Registry
    # Service: chunker (managed)
    runner.invoke(app, [
        "registry", "service", "add", "local-chunker",
        "--image", "my-chunker:latest",
        "--no-input"
    ])
    
    # Service: qdrant (external profile)
    qdrant_path = hsm_sandbox / "hsm-registry" / "services" / "qdrant.yaml"
    runner.invoke(app, [
        "registry", "service", "add", "qdrant",
        "--image", "qdrant/qdrant:latest",
        "--no-input"
    ])
    # Manually patch profile for now (CLI doesn't support profiles yet)
    with open(qdrant_path, "r") as f:
        data = yaml.safe_load(f)
    data["deployment_profiles"]["external-prod"] = {
        "mode": "external",
        "external": {
            "host": "10.0.0.50",
            "port": 6333
        }
    }
    with open(qdrant_path, "w") as f:
        yaml.dump(data, f)

    # 2. Setup Project
    runner.invoke(app, ["init", "--name", "hybrid-cloud-project"])
    
    # Add chunker to a group
    runner.invoke(app, ["registry", "group", "add", "chunker-service", "--type", "service_group", "--option", "local-chunker", "--no-input"])
    runner.invoke(app, ["group", "add", "chunker-service", "--option", "local-chunker"])
    
    # Add qdrant to a group
    runner.invoke(app, ["registry", "group", "add", "vector-db-service", "--type", "service_group", "--option", "qdrant", "--no-input"])
    runner.invoke(app, ["group", "add", "vector-db-service", "--option", "qdrant"])
    
    # Set profile for qdrant
    hsm_yaml_path = hsm_sandbox / "hsm.yaml"
    with open(hsm_yaml_path, "r") as f:
        hsm_data = yaml.safe_load(f)
    # Correct path in hsm.yaml: services -> groups -> <group_name>
    # Note: hsm group add creates 'groups' under 'services'
    hsm_data["services"]["groups"]["vector-db-service"]["profile"] = "external-prod"
    with open(hsm_yaml_path, "w") as f:
        yaml.dump(hsm_data, f)

    # 3. Sync
    result = runner.invoke(app, ["sync", "--no-verify"])
    assert result.exit_code == 0

    # 4. Validate
    compose_path = hsm_sandbox / "docker-compose.hsm.yml"
    assert compose_path.exists()
    with open(compose_path, "r") as f:
        compose_data = yaml.safe_load(f)
    
    # local-chunker should be in compose
    assert "local-chunker" in compose_data["services"]
    # qdrant should NOT be in compose because it's external
    assert "qdrant" not in compose_data["services"]

def test_case_4_editable_stack(runner, hsm_sandbox):
    """Case 4: Editable Stack.
    Library and service from local sources.
    """
    # 1. Create local sources
    pkg_dir = hsm_sandbox / "libs" / "neo4j-client"
    pkg_dir.mkdir(parents=True)
    (pkg_dir / "pyproject.toml").write_text('[project]\nname="neo4j-client"\nversion="0.1.0"')
    
    svc_dir = hsm_sandbox / "services" / "graph-builder"
    svc_dir.mkdir(parents=True)
    (svc_dir / "Dockerfile.dev").write_text("FROM alpine")

    # 2. Setup Registry
    runner.invoke(app, [
        "registry", "library", "add", "neo4j-client",
        "--version", "0.1.0",
        "--prod-type", "local",
        "--dev-path", "libs/neo4j-client",
        "--no-input"
    ])
    
    runner.invoke(app, [
        "registry", "service", "add", "graph-builder-service",
        "--build-path", "services/graph-builder",
        "--dockerfile", "Dockerfile.dev",
        "--runtime", "docker",
        "--no-input"
    ])

    # 3. Setup Project
    runner.invoke(app, ["init", "--name", "editable-project"])
    runner.invoke(app, ["library", "add", "neo4j-client"])
    runner.invoke(app, ["library", "mode", "neo4j-client", "dev"])
    
    runner.invoke(app, ["registry", "group", "add", "graph-services", "--type", "service_group", "--option", "graph-builder-service", "--no-input"])
    runner.invoke(app, ["group", "add", "graph-services", "--option", "graph-builder-service"])
    runner.invoke(app, ["service", "mode", "graph-builder-service", "dev"])

    # 4. Sync
    result = runner.invoke(app, ["sync", "--no-verify"])
    assert result.exit_code == 0

    # 5. Validate
    # Check compose
    compose_path = hsm_sandbox / "docker-compose.hsm.yml"
    if not compose_path.exists():
        print(f"DEBUG: hsm.yaml content:\n{(hsm_sandbox / 'hsm.yaml').read_text()}")
        print(f"DEBUG: Sync output: {result.stdout}")
    assert compose_path.exists()
    with open(compose_path, "r") as f:
        compose_data = yaml.safe_load(f)
    
    svc = compose_data["services"]["graph-builder-service"]
    assert "build" in svc
    assert "Dockerfile.dev" in svc["build"]["dockerfile"]

def test_case_5_secrets(runner, hsm_sandbox, monkeypatch):
    """Case 5: Zero-Leak Secrets.
    Interpolation of environment variables.
    """
    monkeypatch.setenv("NEO4J_PROD_PASSWORD", "secret123")
    monkeypatch.setenv("NEO4J_PROD_PORT", "7687")

    # 1. Setup Registry
    runner.invoke(app, [
        "registry", "service", "add", "graph-builder-service",
        "--image", "graph-builder:latest",
        "--port", "${NEO4J_PROD_PORT}:7474",
        "--env", "DB_PASSWORD=${NEO4J_PROD_PASSWORD}",
        "--runtime", "docker",
        "--no-input"
    ])

    # 2. Setup Project
    runner.invoke(app, ["init", "--name", "secrets-project"])
    runner.invoke(app, ["registry", "group", "add", "graph-services", "--type", "service_group", "--option", "graph-builder-service", "--no-input"])
    runner.invoke(app, ["group", "add", "graph-services", "--option", "graph-builder-service"])

    # 3. Sync
    result = runner.invoke(app, ["sync", "--no-verify"])
    assert result.exit_code == 0

    # 4. Validate
    compose_path = hsm_sandbox / "docker-compose.hsm.yml"
    assert compose_path.exists()
    with open(compose_path, "r") as f:
        compose_data = yaml.safe_load(f)
    
    svc = compose_data["services"]["graph-builder-service"]
    assert svc["environment"]["DB_PASSWORD"] == "${NEO4J_PROD_PASSWORD}"
    assert "${NEO4J_PROD_PORT}:7474" in svc["ports"]