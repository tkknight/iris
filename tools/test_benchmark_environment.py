# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.

"""Tests for ASV benchmark environment preparation."""

import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock


def _load_asv_delegated(monkeypatch, check_output):
    asv_module = ModuleType("asv")
    asv_module.util = SimpleNamespace(check_output=check_output)
    delegated_module = ModuleType("_asv_delegated_abc")
    delegated_module._DelegatedABC = type("_DelegatedABC", (), {})
    monkeypatch.setitem(sys.modules, "asv", asv_module)
    monkeypatch.setitem(sys.modules, "_asv_delegated_abc", delegated_module)

    module_path = Path(__file__).parents[1] / "benchmarks" / "asv_delegated.py"
    spec = importlib.util.spec_from_file_location(
        "asv_delegated_under_test", module_path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_bm_runner():
    module_path = Path(__file__).parents[1] / "benchmarks" / "bm_runner.py"
    spec = importlib.util.spec_from_file_location("bm_runner_under_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prepare_asv_environment_uses_pixi_workspace(tmp_path, monkeypatch):
    checkout_dir = tmp_path / "checkout"
    checkout_dir.mkdir()
    (checkout_dir / "pyproject.toml").write_text("[tool.pixi]\n")
    (checkout_dir / "pixi.lock").write_text("version = 1\n")
    env_parent_dir = tmp_path / "asv" / "env"
    pixi_env_root = env_parent_dir / "pixi"
    expected_prefix = pixi_env_root / "scitools-iris" / "envs"
    check_output = Mock(side_effect=[b"", b"", f"{expected_prefix}\n".encode()])
    asv_delegated = _load_asv_delegated(monkeypatch, check_output)

    result = asv_delegated._prepare_asv_environment(checkout_dir, env_parent_dir)

    assert result == expected_prefix.resolve()
    config_command = check_output.call_args_list[0].args[0]
    assert config_command == [
        "pixi",
        "config",
        "set",
        "--local",
        "detached-environments",
        "true",
    ]
    install_command = check_output.call_args_list[1].args[0]
    assert install_command[:2] == ["pixi", "install"]
    assert "--frozen" in install_command
    assert install_command[install_command.index("--manifest-path") + 1] == str(
        checkout_dir / "pyproject.toml"
    )
    assert install_command[install_command.index("--environment") + 1] == (
        "benchmark-py314"
    )
    assert check_output.call_args_list[1].kwargs["env"][
        "PIXI_CACHE_DETACHED_ENVIRONMENTS_DIR"
    ] == str(pixi_env_root)


def test_prepare_asv_environment_uses_historical_lock(tmp_path, monkeypatch):
    checkout_dir = tmp_path / "checkout"
    lock_dir = checkout_dir / "requirements" / "locks"
    lock_dir.mkdir(parents=True)
    (lock_dir / "py312-linux-64.lock").write_text("@EXPLICIT\n")
    (lock_dir / "py314-linux-64.lock").write_text("@EXPLICIT\n")
    env_parent_dir = tmp_path / "asv" / "env"
    check_output = Mock(return_value=b"")
    asv_delegated = _load_asv_delegated(monkeypatch, check_output)

    result = asv_delegated._prepare_asv_environment(checkout_dir, env_parent_dir)

    expected_prefix = env_parent_dir / "conda-py314"
    assert result == expected_prefix.resolve()
    conda_command = check_output.call_args_list[0].args[0]
    assert conda_command[:2] == ["conda", "create"]
    assert conda_command[conda_command.index("--file") + 1] == str(
        lock_dir / "py314-linux-64.lock"
    )
    assert conda_command[conda_command.index("--prefix") + 1] == str(expected_prefix)
    install_command = check_output.call_args_list[1].args[0]
    assert install_command[:3] == ["conda", "run", "--prefix"]
    assert "--no-deps" in install_command
    assert install_command[-1] == str(checkout_dir)


def test_prep_data_gen_env_uses_pixi_environment(tmp_path, monkeypatch):
    bm_runner = _load_bm_runner()

    python_path = tmp_path / "pixi" / "scitools-iris" / "envs" / "bin" / "python"
    python_path.parent.mkdir(parents=True)
    python_path.touch()
    monkeypatch.delenv("DATA_GEN_PYTHON", raising=False)
    monkeypatch.setenv("OVERRIDE_TEST_DATA_REPOSITORY", str(tmp_path / "test_data"))
    run = Mock()
    run_capture = Mock(return_value=str(python_path))
    monkeypatch.setattr(bm_runner, "_subprocess_runner", run)
    monkeypatch.setattr(bm_runner, "_subprocess_runner_capture", run_capture)

    bm_runner._prep_data_gen_env()

    assert run.call_args_list[0].args[0] == [
        "pixi",
        "install",
        "--frozen",
        "--environment",
        "data-py314",
    ]
    assert run_capture.call_args.args[0] == [
        "pixi",
        "run",
        "--frozen",
        "--environment",
        "data-py314",
        "python",
        "-c",
        "import sys; print(sys.executable)",
    ]
    assert bm_runner.environ["DATA_GEN_PYTHON"] == str(python_path.resolve())
