# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Repository-specific adaptation of :mod:`_asv_delegated_abc`."""

from os import environ
from pathlib import Path
import re

from asv import util as asv_util

from _asv_delegated_abc import _DelegatedABC


def _prepare_asv_environment(checkout_dir: Path, env_parent_dir: Path) -> Path:
    """Prepare the environment for a current or historical Iris checkout."""
    env_parent_dir.mkdir(parents=True, exist_ok=True)
    manifest = checkout_dir / "pyproject.toml"
    lockfile = checkout_dir / "pixi.lock"

    if manifest.is_file() and lockfile.is_file():
        pixi_env_root = env_parent_dir / "pixi"
        local_envs = dict(environ)
        local_envs["PIXI_CACHE_DETACHED_ENVIRONMENTS_DIR"] = str(pixi_env_root)
        asv_util.check_output(
            ["pixi", "config", "set", "--local", "detached-environments", "true"],
            cwd=checkout_dir,
            env=local_envs,
        )
        asv_util.check_output(
            [
                "pixi",
                "install",
                "--frozen",
                "--manifest-path",
                str(manifest),
                "--environment",
                "benchmark-py314",
            ],
            cwd=checkout_dir,
            env=local_envs,
        )
        prefix = asv_util.check_output(
            [
                "pixi",
                "run",
                "--frozen",
                "--manifest-path",
                str(manifest),
                "--environment",
                "benchmark-py314",
                "python",
                "-c",
                "import sys; print(sys.prefix)",
            ],
            cwd=checkout_dir,
            env=local_envs,
        )
        return Path(prefix.decode().strip()).resolve()

    lock_dir = checkout_dir / "requirements" / "locks"
    locks_by_version = {
        int(match.group(1)): lock
        for lock in lock_dir.glob("py*-linux-64.lock")
        if (match := re.fullmatch(r"py(\d+)-linux-64\.lock", lock.name))
    }
    if not locks_by_version:
        message = f"No explicit Conda lockfiles found in {lock_dir}."
        raise FileNotFoundError(message)

    version, lockfile = max(locks_by_version.items())
    prefix = env_parent_dir / f"conda-py{version}"
    asv_util.check_output(
        [
            "conda",
            "create",
            "--yes",
            "--prefix",
            str(prefix),
            "--file",
            str(lockfile),
        ],
        cwd=checkout_dir,
    )
    asv_util.check_output(
        [
            "conda",
            "run",
            "--prefix",
            str(prefix),
            "python",
            "-m",
            "pip",
            "install",
            "--no-deps",
            "-e",
            str(checkout_dir),
        ],
        cwd=checkout_dir,
    )
    return prefix.resolve()


class Delegated(_DelegatedABC):
    """Specialism of :class:`_DelegatedABC` for benchmarking this repo."""

    tool_name = "delegated"

    def _prep_env_override(self, env_parent_dir: Path) -> Path:
        """Environment preparation specialised for this repo.

        Scans the checked-out commit of Iris to work out the appropriate
        preparation command, including gathering any extra information that said
        command needs.

        Parameters
        ----------
        env_parent_dir : Path
            The directory that the prepared environment should be placed in.

        Returns
        -------
        Path
            The path to the prepared environment.
        """
        # The project checkout.
        build_dir = Path(self._build_root) / self._repo_subdir

        # Older iterations of setup.py are incompatible with setuptools>=80.
        #  (Most dependencies are protected by lock-files, but build
        #   dependencies in pyproject.toml are independent).
        setup_py = build_dir / "setup.py"
        pyproject = build_dir / "pyproject.toml"
        if setup_py.is_file() and "setuptools.command.develop" in setup_py.read_text():
            with pyproject.open("r+") as file_write:
                lines = file_write.readlines()
                for i, line in enumerate(lines):
                    if line == "requires = [\n":
                        next_line = lines[i + 1]
                        indent = next_line[: len(next_line) - len(next_line.lstrip())]

                        lines.insert(i + 1, f'{indent}"setuptools<80",\n')
                        break
                file_write.seek(0)
                file_write.writelines(lines)

        return _prepare_asv_environment(build_dir, env_parent_dir)
