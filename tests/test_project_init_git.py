import subprocess
from hyper_stack_manager.cli.root import app


def test_library_init_with_git_init_creates_repo(runner, hsm_sandbox):
    """GIT-HF-001: library init with --git-init creates .git directory."""
    runner.invoke(app, ["init"])
    result = runner.invoke(app, ["library", "init", "git-lib", "--git-init"])

    assert result.exit_code == 0
    assert (hsm_sandbox / "packages" / "git-lib" / ".git").exists()


def test_service_init_with_git_init_creates_repo(runner, hsm_sandbox):
    """GIT-HF-002: service init with --git-init creates .git directory."""
    runner.invoke(app, ["init"])
    result = runner.invoke(app, ["service", "init", "git-service", "--runtime", "uv", "--git-init"])

    assert result.exit_code == 0
    assert (hsm_sandbox / "services" / "git-service" / ".git").exists()


def test_init_without_git_init_does_not_create_repo(runner, hsm_sandbox):
    """GIT-HF-003: without --git-init no .git directory is created."""
    runner.invoke(app, ["init"])

    lib_result = runner.invoke(app, ["library", "init", "plain-lib"])
    svc_result = runner.invoke(app, ["service", "init", "plain-service", "--runtime", "uv"])

    assert lib_result.exit_code == 0
    assert svc_result.exit_code == 0
    assert not (hsm_sandbox / "packages" / "plain-lib" / ".git").exists()
    assert not (hsm_sandbox / "services" / "plain-service" / ".git").exists()


def test_library_init_git_binary_missing_fails(runner, hsm_sandbox, monkeypatch):
    """GIT-FAIL-001: command fails if git binary is not available."""
    runner.invoke(app, ["init"])

    real_run = subprocess.run

    def selective_run(*args, **kwargs):
        cmd = args[0] if args else kwargs.get("args")
        if cmd == ["git", "init"]:
            raise FileNotFoundError("git not found")
        return real_run(*args, **kwargs)

    monkeypatch.setattr(subprocess, "run", selective_run)

    result = runner.invoke(app, ["library", "init", "broken-lib", "--git-init"])

    assert result.exit_code != 0
    assert "git binary is not available" in result.stdout


def test_service_init_git_init_error_fails(runner, hsm_sandbox, monkeypatch):
    """GIT-FAIL-002: command fails if git init returns non-zero code."""
    runner.invoke(app, ["init"])

    real_run = subprocess.run

    def selective_run(*args, **kwargs):
        cmd = args[0] if args else kwargs.get("args")
        if cmd == ["git", "init"]:
            raise subprocess.CalledProcessError(returncode=1, cmd=cmd)
        return real_run(*args, **kwargs)

    monkeypatch.setattr(subprocess, "run", selective_run)

    result = runner.invoke(app, ["service", "init", "broken-service", "--runtime", "docker", "--git-init"])

    assert result.exit_code != 0
    assert "git init failed" in result.stdout.lower()
