# Iris Pixi Support Design

Date: 2026-09-11
Status: Approved in chat, pending file-level review
Owner: Contributors

## 1. Goal

Extend Iris packaging and contributor workflow documentation to support Pixi, while preserving existing conda and pip workflows.

This phase is additive and low-risk:
- Add Pixi as a first-class documented option for users and contributors.
- Add a repository Pixi manifest and useful tasks.
- Keep current conda requirements files and conda-lock flow as source-of-truth and CI baseline.

## 2. Decisions Already Approved

1. Pixi should support both:
- Contributor workflow
- End-user install path

2. Lockfile strategy for this phase:
- Do not introduce pixi.lock automation in CI yet.
- Allow local Pixi resolution for now.

3. Dependency authority model:
- Pixi remains secondary mirror.
- Existing requirements/*.yml and conda lock pipeline remain primary.

## 3. Constraints and Existing System

Current Iris packaging and CI conventions:
- Conda requirement manifests live in requirements/*.yml.
- Reproducible CI envs use requirements/locks/*.lock.
- Lock refresh is handled by .github/workflows/refresh-lockfiles.yml.
- nox is configured with conda backend in noxfile.py.
- Existing install docs mention conda and pip, no Pixi option today.

Design must not disrupt this baseline.

## 4. Scope

In scope:
- Add Pixi documentation to user install docs.
- Add Pixi documentation to contributor/developer docs where environment setup and test running are explained.
- Add root pixi.toml manifest with practical environments and tasks.
- Keep compatibility with current manual pytest workflow and nox workflow.

Out of scope:
- Replacing nox conda backend with Pixi.
- Replacing requirements/*.yml as primary dependency source.
- Introducing Pixi lock refresh automation in GitHub Actions.
- Enforcing pixi.lock in CI.

## 5. Proposed Artifact Changes

1. New file:
- pixi.toml

2. Documentation updates:
- docs/src/user_manual/how_to/installing.rst
- docs/src/developers_guide/contributing_running_tests.rst
- docs/src/developers_guide/contributing_ci_tests.rst
- Possibly docs/src/developers_guide/contributing_code_formatting.rst if setup assumptions need Pixi alternative wording.

3. No CI workflow edits in this phase.

## 6. Pixi Manifest Design

### 6.1 Workspace

- channel: conda-forge
- platform: linux-64 (aligned with currently tested platform)

### 6.2 Environments

- default:
  - Purpose: basic user install/use path.
  - Minimal runtime dependencies for import/use.

- dev:
  - Purpose: contributor flow.
  - Includes tooling used by docs/tests workflows.
  - Uses editable local install for Iris.

Optional follow-up environments may be added later if needed:
- docs
- tests

This phase can start with default + dev only to keep maintenance cost low.

### 6.3 Tasks

Tasks should provide convenience, not replace existing commands.

Candidate tasks:
- tests-unit: run pytest against lib/iris
- tests-fast: run non-slow subset if marker policy exists
- docs-html: build docs from docs directory
- docs-doctest: run doctests
- lint: run ruff checks

Task names should be explicit and consistent with existing contributor language.

## 7. Data and Dependency Flow

Dependency source flow for this phase:
1. requirements/*.yml remains canonical contributor baseline for CI and lock refresh.
2. pixi.toml mirrors practical dependency intent for local Pixi users.
3. Any mismatch is fixed by updating pixi.toml, unless there is a broader packaging policy decision.

No conversion/export pipeline is added in this phase.

## 8. Failure Handling

Potential failure modes and handling:

1. Pixi solve failure on contributor machine:
- Keep conda/nox instructions as stable fallback in same docs sections.

2. Drift between pixi.toml and requirements/*.yml:
- Treat as maintenance issue in pixi mirror.
- Correct pixi.toml without changing CI baseline.

3. Confusion about official CI path:
- Explicitly document that CI continues to use conda requirement files and lockfiles.

## 9. Testing and Verification Plan

Verification required before completion claim:

1. Documentation checks:
- New Pixi instructions are syntactically correct and consistent with current docs style.
- Existing conda/pip instructions remain intact.

2. Local Pixi smoke checks:
- Create default environment and import iris.
- Create dev environment and run at least one targeted test command.
- Run one docs-related task successfully (or report exact limitation).

3. Regression checks:
- Ensure no nox command behavior changed.
- Ensure no CI workflow files changed unintentionally.

## 10. Rollout and Future Work

Future phase candidates:
- Add pixi.lock to repository policy.
- Add Pixi lock refresh CI workflow.
- Optionally export conda artifacts from Pixi as part of a source-of-truth migration.

Any migration of dependency authority from requirements/*.yml to Pixi requires separate explicit approval.

## 11. Acceptance Criteria

This design is accepted for implementation when:
- Pixi added as documented user and contributor path.
- Root pixi.toml exists and supports practical local usage.
- Existing conda/pip docs still valid and present.
- Existing CI lockfile and nox conda workflows unchanged.
- Verification evidence captured in implementation response.
