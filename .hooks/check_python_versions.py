# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.

"""Pre-commit hook: ensure Python versions are consistent across config files.

Supported Python versions must have matching Pixi environments and CI entries.

This hook runs when any version-related file is modified and validates that
all versions are in sync across the entire repository.

Usage (pre-commit passes staged file paths as arguments)::

    python .hooks/check_python_versions.py [file ...]

Exit codes:
    0 – all versions are consistent
    1 – version inconsistencies detected
"""

from pathlib import Path
import re
import sys
import tomllib

from packaging.version import Version

# Files that contain Python version information
_VERSION_CONFIG_FILES = {
    "pyproject.toml",
    ".github/workflows/ci-wheels.yml",
    ".github/workflows/ci-tests.yml",
    "benchmarks/bm_runner.py",
}


def _find_repo_root(start_path: Path) -> Path:
    """Find the repository root by looking for .git."""
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return start_path


def _extract_supported_versions(root_dir: Path) -> list[str] | None:
    """Extract supported Python versions from pyproject.toml.

    Returns None if versions cannot be determined.
    """
    pyproject = root_dir / "pyproject.toml"
    if not pyproject.exists():
        return None

    try:
        with pyproject.open("rb") as stream:
            config = tomllib.load(stream)
        classifiers = config.get("project", {}).get("classifiers", [])
        matches = [
            match.group(1)
            for classifier in classifiers
            if (
                match := re.fullmatch(
                    r"Programming Language :: Python :: (3\.\d+)", classifier
                )
            )
        ]
        if matches:
            return sorted(set(matches))
    except (OSError, UnicodeDecodeError):
        pass
    except tomllib.TOMLDecodeError:
        return None

    return None


def check_consistency(root_dir: Path) -> list[str]:
    """Check that Python versions are consistent across all config files.

    Returns a list of violation strings, empty if all consistent.
    """
    # Get the authoritative version list from pyproject.toml
    all_supported = _extract_supported_versions(root_dir)
    if not all_supported:
        # Can't validate without knowing what versions should be supported
        return []

    _parsed = [Version(v) for v in all_supported]
    latest_supported = str(max(_parsed))

    pyproject_toml_file = root_dir / "pyproject.toml"
    with pyproject_toml_file.open("rb") as stream:
        config = tomllib.load(stream)
    environments = config.get("tool", {}).get("pixi", {}).get("environments", {})

    violations = []
    required_environments = {
        f"{kind}-py{version.replace('.', '')}"
        for version in all_supported
        for kind in ("dev", "test", "wheel")
    }
    required_environments.update(
        {
            f"docs-py{latest_supported.replace('.', '')}",
            f"benchmark-py{latest_supported.replace('.', '')}",
            f"data-py{latest_supported.replace('.', '')}",
            f"release-py{latest_supported.replace('.', '')}",
        }
    )
    for environment in sorted(required_environments - environments.keys()):
        violations.append(
            f"{pyproject_toml_file}: missing Pixi environment {environment}"
        )

    ci_wheels_file = root_dir / ".github" / "workflows" / "ci-wheels.yml"
    if ci_wheels_file.exists():
        workflow_environments = set(
            re.findall(
                r"^\s*pixi-environment:\s*([^\s#]+)",
                ci_wheels_file.read_text(),
                re.MULTILINE,
            )
        )
        required = {f"wheel-py{version.replace('.', '')}" for version in all_supported}
        for environment in sorted(required - workflow_environments):
            violations.append(
                f"{ci_wheels_file}: missing CI Pixi environment {environment}"
            )

    ci_tests_file = root_dir / ".github" / "workflows" / "ci-tests.yml"
    if ci_tests_file.exists():
        workflow_environments = set(
            re.findall(
                r"^\s*pixi-environment:\s*([^\s#]+)",
                ci_tests_file.read_text(),
                re.MULTILINE,
            )
        )
        required = {f"test-py{version.replace('.', '')}" for version in all_supported}
        required.add(f"docs-py{latest_supported.replace('.', '')}")
        for environment in sorted(required - workflow_environments):
            violations.append(
                f"{ci_tests_file}: missing CI Pixi environment {environment}"
            )

    return violations


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # Find repository root
    if not argv:
        # No files provided, can't determine repo root
        # In this case, do nothing (let normal test handle it)
        return 0

    paths = [Path(p) for p in argv]
    repo_root = _find_repo_root(paths[0])

    # Check if any of the version-related files are in the staged files
    is_version_file_staged = any(
        str(p).endswith(tuple(f"/{name}" for name in _VERSION_CONFIG_FILES))
        or str(p).endswith(tuple(_VERSION_CONFIG_FILES))
        for p in paths
    )

    if not is_version_file_staged:
        # Only run check if a version-related file is being modified
        return 0

    violations = check_consistency(repo_root)

    if violations:
        print(
            "Python version consistency check failed.\n"
            "Python versions must be updated consistently across all config files.\n"
        )
        for v in violations:
            print(v)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
