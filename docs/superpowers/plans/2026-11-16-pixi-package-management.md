# Pixi Package Management Implementation Plan

> **For agentic workers:** Implement task by task. Steps use checkbox syntax.

**Goal:** Replace Iris development and CI environment management with Pixi while
preserving published PyPI metadata and historical ASV benchmark environments.

**Architecture:** Declare the active environments, Conda/PyPI dependencies,
and tasks in `pyproject.toml`, with one committed `pixi.lock`. Migrate CI and
the benchmark runner to Pixi; let ASV use historical explicit Conda lockfiles
only for checked-out revisions that predate Pixi.

**Tech Stack:** Pixi, Conda, PyPI, Python, pytest, ASV, GitHub Actions,
Sphinx.

**Spec:** `docs/superpowers/specs/2026-11-16-pixi-package-management-design.md`

## Global Constraints

- Support Python 3.12, 3.13, and 3.14.
- Use conda-forge packages where suitable; use Pixi PyPI dependencies where a
  package should come from PyPI.
- Keep `requirements/pypi-core.txt` as the source of published runtime
  dependency metadata.
- Do not add a custom synchronization generator for PyPI metadata and Pixi.
- Keep supported environments and CI lock targets on `linux-64`.
- Preserve optional packages currently used by CI tests.
- Preserve the Git-sourced `nothing` test dependency and ASV benchmark tools.
- Preserve per-commit ASV environments for pre-Pixi revisions without Nox.
- Keep `requirements/readthedocs.yml` unchanged.
- Use `iris-dev` for local checks; do not install or remove packages from it.
- Set and verify `OVERRIDE_TEST_DATA_REPOSITORY` before trusting Iris test
  results; inspect skip counts for lost coverage.
- Update the root and test `AGENTS.md` setup guidance as explicitly approved;
  retain their change-control meta-instructions.

## Review Focus

- Python-version support remains synchronized between package classifiers,
  Pixi environments, and CI matrices. Pin this in the existing coding
  standards test.
- Test environments retain optional integrations so Pixi does not increase
  skipped coverage. Pin this by comparing the test environment packages with
  the current CI package set and inspecting test skips.
- Published wheels continue to install from PyPI metadata rather than relying
  on the editable development install. Pin this in the wheel CI task.
- Frozen CI installs fail when the committed lock is stale. Pin this with
  `pixi install --locked` and frozen task runs.
- ASV uses each historical revision's own lockfile without Nox, while the
  current revision uses Pixi. Pin both branches with isolated tests of the
  benchmark environment setup helper.

---

### Task 1: Define Pixi environments and lock

**Files:**
- Modify: `pyproject.toml`
- Create: `pixi.lock`
- Read-only reference: `environment.yml`, `requirements/py312.yml`,
  `requirements/py313.yml`, `requirements/py314.yml`,
  `requirements/pypi-core.txt`

**Interfaces:**
- Produces environments for Python 3.12, 3.13, and 3.14, separated into
  development, test, documentation, benchmark, and existing optional-package
  groups.
- Use a distinct solve group for each Python version. Name environments
  consistently, such as `dev-py312`, `test-py312`, and `docs-py312`.
- Provides editable Iris installation in development environments.
- Test environments retain the `nothing` dependency currently installed from
  `SciTools-incubator/nothing`; the benchmark environment includes ASV.
- Preserve GeoVista in the Python 3.12 and 3.13 optional environments, and
  leave it disabled in Python 3.14 environments as in the current files.

- [ ] Map current Conda dependencies into Pixi Conda dependencies and PyPI
  dependencies into Pixi `pypi-dependencies`; preserve version constraints and
  platform-specific exceptions.
- [ ] Add Python-version features and the per-version environments to
  `[tool.pixi]`; include current CI optional dependencies in test environments.
- [ ] Declare the Git-sourced `nothing` dependency in test environments and
  ASV in the benchmark environment.
- [ ] Run `pixi update` to create `pixi.lock` for `linux-64`.
- [ ] Run `pixi install --locked --environment <environment>` for each
  environment; expected: every declared environment resolves from the
  manifest and lock without changing `pixi.lock`.
- [ ] Run `pixi run --frozen --environment dev-py314 python -c "import iris"`;
  expected: the editable source checkout imports successfully.

### Task 2: Add Pixi tasks and contributor guidance

**Files:**
- Modify: `pyproject.toml`
- Modify: `docs/src/user_manual/how_to/installing.rst`
- Modify: `docs/src/developers_guide/contributing_running_tests.rst`
- Modify: `docs/src/developers_guide/contributing_ci_tests.rst`
- Modify: `docs/src/developers_guide/github_app.rst`
- Modify: `docs/src/developers_guide/release.rst`
- Modify: `benchmarks/README.md`, `benchmarks/custom_bms/README.md`

**Interfaces:**
- Produces Pixi tasks for tests, doctests, gallery tests, wheel checks, and
  benchmark runner commands.
- Contributor examples use `pixi run --environment <name> <task>`.

- [ ] Define test, doctest, gallery, wheel, and benchmark tasks using the
  commands currently run by Nox; keep pytest targets and coverage arguments
  unchanged.
- [ ] Document Pixi installation, environment selection, common task commands,
  and `pixi update` for lock refresh.
- [ ] Replace the Nox instructions in the test guide with Pixi instructions;
  replace root `environment.yml` setup instructions in the source-install
  guide with the default Pixi environment.
- [ ] Update CI, GitHub App, release, and benchmark guidance to describe Pixi
  environments and tasks. Keep historical release notes unchanged.
- [ ] Run `pre-commit run --files` for changed documentation and
  `pixi run --environment docs-py314 doctest`; expected: hooks pass and Sphinx
  doctests complete without new warnings or errors.

### Task 3: Migrate test, docs, and wheel CI

**Files:**
- Modify: `.github/workflows/ci-tests.yml`
- Modify: `.github/workflows/ci-wheels.yml`
- Remove: `.github/workflows/composite/nox-cache/action.yml`

**Interfaces:**
- Test matrix remains Python 3.12, 3.13, and 3.14; doctests and gallery use
  Python 3.14.
- CI installs named Pixi environments in frozen mode and invokes Pixi tasks.
- Cartopy and Iris test-data caches remain available.

- [ ] Replace setup-miniconda, conda environment setup, and Nox environment
  cache steps with the pinned Pixi setup action and its supported environment
  caching configuration.
- [ ] Run unit, integration, and system tests through the matching Python test
  environment; retain `-n auto`, coverage, and test-data configuration.
- [ ] Run doctests and gallery tests through the Python 3.14 documentation
  environment.
- [ ] Run wheel installation tests through Pixi after downloading the built
  artifact; install the wheel using its declared package metadata, not the
  editable development dependency.
- [ ] Run YAML/pre-commit checks for both workflows; expected: actions pass
  configuration and security checks, and existing CI matrix coverage remains.

### Task 4: Replace lock refresh workflow

**Files:**
- Modify: `.github/workflows/refresh-lockfiles.yml`
- Modify: `requirements/README.md`
- Remove: `requirements/locks/README.md`

**Interfaces:**
- The scheduled and manually dispatched workflow runs `pixi update` and opens
  a pull request only when `pixi.lock` changes.
- Existing GitHub App authentication remains able to trigger the CI workflows
  for the generated pull request.

- [ ] Replace the reusable conda-lock workflow with Pixi setup and lock update
  steps; retain schedule and workflow-dispatch triggers.
- [ ] Detect lock changes before invoking create-pull-request; limit its
  changed paths to `pixi.lock`.
- [ ] Update dependency documentation to describe Pixi and the generated lock.
- [ ] Check the workflow with pre-commit and `zizmor`; expected: valid actions,
  least-privilege permissions, and no pull request when the lock is unchanged.

### Task 5: Migrate ASV environment preparation

**Files:**
- Modify: `benchmarks/asv_delegated.py`
- Modify: `benchmarks/bm_runner.py`
- Add tests: `tools/test_benchmark_environment.py`
- Modify: `benchmarks/README.md`

**Interfaces:**
- Replace `Delegated._prep_env_override(self, env_parent_dir: Path) -> Path`
  Nox detection with Pixi detection for current revisions and direct Conda
  lock installation for pre-Pixi revisions.
- Add `_prepare_asv_environment(checkout_dir: Path, env_parent_dir: Path) -> Path`
  in `benchmarks/asv_delegated.py`; it returns the Pixi prefix for a current
  checkout or the created Conda prefix for a historical checkout.
- Preserve `_prep_data_gen_env() -> None` behavior, including
  `DATA_GEN_PYTHON`, Mule, and test-data setup.
- Keep environment creation inside ASV's environment directory.

- [ ] Add `test_prepare_asv_environment_uses_pixi_workspace` and
  `test_prepare_asv_environment_uses_historical_lock` to
  `tools/test_benchmark_environment.py`. Assert current checkouts use their
  manifest and frozen lock; historical checkouts use their explicit lock and
  install Iris with `--no-deps`.
- [ ] Run `pytest tools/test_benchmark_environment.py`; expected: both tests
  fail because `_prepare_asv_environment` does not yet exist.
- [ ] Implement `_prepare_asv_environment(checkout_dir, env_parent_dir)` and
  call it from `Delegated._prep_env_override`; remove AST inspection of
  `noxfile.py` and return the resolved prefix for ASV's delegated symlink.
- [ ] Run `pytest tools/test_benchmark_environment.py`; expected: both tests
  pass without network access.
- [ ] Replace the data-generation Nox `--install-only` call with the named
  Pixi data-generation environment; keep Mule, `iris-test-data`, and reuse
  behavior unchanged.
- [ ] Remove Nox from `_setup_common` requirements; retain ASV validation and
  benchmark runner behavior.
- [ ] Run the benchmark environment tests again; expected: current and
  historical setup remains Nox-free.

### Task 6: Migrate benchmark CI

**Files:**
- Modify: `.github/workflows/benchmarks_run.yml`
- Modify: `.github/workflows/benchmarks_validate.yml`
- Modify: `.github/labeler.yml`
- Modify: `benchmarks/README.md`
- Modify: `benchmarks/custom_bms/README.md`

**Interfaces:**
- Benchmark commands run through the named Pixi benchmark task.
- ASV continues to cache its environments and results; Conda package caches
  remain only where historical lock installation needs them.

- [ ] Replace Nox installation and commands with the Pixi setup action and
  benchmark task; preserve overnight, pull-request, validation, and artifact
  behavior.
- [ ] Change the benchmark pull-request trigger from `requirements/locks/*.lock`
  to `pixi.lock` and update labeler patterns.
- [ ] Remove `.nox` from benchmark caches; retain `.asv/env`, benchmark data,
  and any Conda cache needed for pre-Pixi commits.
- [ ] Run workflow pre-commit and `zizmor`; expected: no Nox commands remain in
  active benchmark workflows.

### Task 7: Remove obsolete environment and Nox machinery

**Files:**
- Remove: `noxfile.py`, `environment.yml`, `tools/update_lockfiles.py`,
  `requirements/py312.yml`, `requirements/py313.yml`,
  `requirements/py314.yml`, and current `requirements/locks/*.lock`
- Modify: `Makefile`, `MANIFEST.in`, `.gitignore`, `pyrightconfig.json`,
  `.pre-commit-config.yaml`, `.hooks/check_python_versions.py`,
  `lib/iris/tests/test_coding_standards.py`, `AGENTS.md`,
  `lib/iris/tests/AGENTS.md`
- Remove: `.github/workflows/composite/nox-cache/action.yml`
- Add: one `internal` changelog fragment for the contributor workflow change

**Interfaces:**
- The Python-version consistency hook reads Pixi environment definitions and
  CI matrices, not Nox or Conda YAML files.
- `requirements/readthedocs.yml` and all PyPI runtime/optional metadata remain.

- [ ] Update `test_python_versions` to require matching Pixi environment
  entries for each supported classifier; add a focused fixture test showing a
  missing Python environment is reported.
- [ ] Run `pytest lib/iris/tests/test_coding_standards.py::test_python_versions`;
  expected: the new missing-environment case fails before the hook changes.
- [ ] Update `check_python_versions.py` and its pre-commit file filter to
  validate Pixi environments and CI entries instead of Nox and Conda YAML.
- [ ] Run `pytest lib/iris/tests/test_coding_standards.py::test_python_versions`;
  expected: all supported Python versions pass and the missing-environment
  case is detected.
- [ ] Remove Nox-specific Makefile, manifest, ignore, type-checker, and
  pre-commit configuration; remove active environment YAML and lock files.
- [ ] Update root and test `AGENTS.md` setup and test commands to Pixi; retain
  their meta-instructions and all unrelated guidance.
- [ ] Add the internal changelog fragment and update any remaining active
  documentation that directs contributors to Nox or Conda setup. Preserve
  historical release notes and the Nox reference needed by them.
- [ ] Search tracked files for active references to `noxfile.py`, Nox
  commands, `environment.yml`, `requirements/py*.yml`, and conda-lock. Expected:
  none outside historical release notes and historical ASV lock handling.
- [ ] Run `pre-commit run --all-files`, `pixi run --environment test-py314
  tests`, `pixi run --environment docs-py314 doctest`, and the Pixi gallery
  task; inspect skips and compare them with the current CI optional coverage.

## Handoff Notes

- Run Pixi commands from the repository root. Do not install Pixi into or
  alter the existing `iris-dev` environment.
- No task requires committing changes unless the user requests commits.