# Ruff Rule Adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable and adopt three pydocstyle rules (D101, D102, D103) one at a time, fixing all violations, committing per rule, and creating one PR per rule.

**Architecture:** Each rule gets its own cycle: enable in `pyproject.toml`, run ruff to enumerate violations, fix all occurrences (add docstrings or suppress with `# noqa`), validate with pre-commit, commit, and push a PR. Order: D101 (class docstrings) → D102 (method docstrings) → D103 (function docstrings). This validates the workflow with early wins before tackling larger rule families.

**Tech Stack:** Python, ruff linter, pytest, pre-commit, git.

**Spec:** [`docs/superpowers/specs/2026-11-17-ruff-rule-adoption-design.md`](../specs/2026-11-17-ruff-rule-adoption-design.md)

## Global Constraints

- **Python versions:** 3.12, 3.13, 3.14 (all must remain compatible)
- **Line length:** 88 characters (Ruff default, enforced by pre-commit)
- **Docstring style:** NumPy style, strictly validated
- **Copyright header:** Every new Python file must include the BSD-3-Clause header
- **Commits:** Include `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer
- **GitHub posts:** Prefix with `(posted by Claude Opus)` on issues, PRs, and comments

## Review Focus

1. **Docstring accuracy:** Docstrings added should accurately describe the class/method/function behavior; copy-paste placeholders or vague descriptions defeat the purpose.
2. **Legitimate suppression:** Some public classes/methods/functions may intentionally have no docstring (e.g., private test helpers). Verify `# noqa: D10x` is used only for deliberate exceptions, not convenience.
3. **NumPy style compliance:** All added docstrings must follow NumPy docstring conventions (Parameters, Returns, Raises, Examples sections). The linter will catch format issues, but semantic correctness is a judgment call.
4. **Lazy data handling:** When documenting Cube methods, ensure docstrings note whether data materialization occurs (avoid calling `.data` unnecessarily per AGENTS.md Critical Gotcha #4).
5. **Existing test coverage:** Fixing violations in test files should not require docstrings (pydocstyle excludes tests by default); if violations appear in test code, check the per-file-ignores config.

---

## Task 1: Enable D101 (Missing docstring in public class)

**Files:**
- Modify: `pyproject.toml:211–225` (remove `D101` from ignore list)
- Modify: Multiple class definitions in `lib/iris/` (add docstrings or `# noqa: D101`)
- Test: Run ruff checks and pre-commit validation

**Interfaces:**
- Consumes: Current `pyproject.toml` with D101 in the ignore list
- Produces: Updated `pyproject.toml` with D101 enabled; all public classes either documented or explicitly exempted

**Steps:**

- [ ] **Step 1: Identify D101 violations**

Run:
```bash
cd /home/users/tremain.knight/projects/iris
ruff check --select "D101" lib/iris --statistics
```

Expected output: A list of files and line numbers with public classes missing docstrings, plus a count of violations. Record the count for the PR description.

- [ ] **Step 2: Enable D101 in pyproject.toml**

Edit `pyproject.toml` lines 211–225 (`[tool.ruff.lint] ignore` list). Remove the line:
```python
"D101",  # Missing docstring in public class
```

Save the file. Do NOT fix violations yet.

- [ ] **Step 3: Run ruff again to confirm D101 is active**

Run:
```bash
ruff check --select "D101" lib/iris --statistics
```

Expected: Same violations listed (rule is now active, not ignored).

- [ ] **Step 4: Fix all D101 violations**

For each violation, examine the class and add a docstring using NumPy style. If the class is intentionally undocumented (rare), add `# noqa: D101` above the class definition instead.

**Decision rule:** Add a docstring unless the class is a known test helper or internal implementation detail already documented elsewhere. When in doubt, document it.

No script needed—iterate through the violations list from Step 1 and edit each file. Use this template:

```python
class ClassName:
    """
    Brief one-line description.

    Optional longer description explaining purpose, usage, or relationship
    to other classes.
    """
```

- [ ] **Step 5: Run pre-commit to validate docstrings and formatting**

Run:
```bash
pre-commit run --files lib/iris --all-files
```

Expected: All hooks pass, or return errors for invalid docstring format (which you fix immediately).

- [ ] **Step 6: Run ruff one more time to confirm zero D101 violations**

Run:
```bash
ruff check --select "D101" lib/iris --statistics
```

Expected: No violations reported.

- [ ] **Step 7: Commit**

Run:
```bash
git add pyproject.toml lib/iris
git commit -m "Enable ruff rule D101: missing docstring in public class

Add docstrings to <N> public classes to comply with D101.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

(Replace `<N>` with the count from Step 1.)

- [ ] **Step 8: Create a pull request**

Run:
```bash
gh pr create --title "Enable D101: missing docstring in public class" \
  --body "(posted by Claude Opus)

Enable the D101 pydocstyle rule and add docstrings to <N> public classes.

This is part of the ruff rule adoption plan to progressively enable ignored rules. See the spec: docs/superpowers/specs/2026-11-17-ruff-rule-adoption-design.md"
```

(Replace `<N>` with the count from Step 1; adjust body as needed.)

---

## Task 2: Enable D102 (Missing docstring in public method)

**Files:**
- Modify: `pyproject.toml:214–215` (remove `D102` from ignore list)
- Modify: Multiple method definitions in `lib/iris/` (add docstrings or `# noqa: D102`)
- Test: Run ruff checks and pre-commit validation

**Interfaces:**
- Consumes: Completed Task 1 (D101 rule enabled and all violations fixed); updated `pyproject.toml`
- Produces: Updated `pyproject.toml` with D102 enabled; all public methods either documented or explicitly exempted

**Steps:**

- [ ] **Step 1: Identify D102 violations**

Run:
```bash
ruff check --select "D102" lib/iris --statistics
```

Expected output: A list of files and line numbers with public methods missing docstrings, plus a count of violations. Record the count for the PR description.

- [ ] **Step 2: Enable D102 in pyproject.toml**

Edit `pyproject.toml` to remove the line:
```python
"D102",  # Missing docstring in public method
```

Save the file. Do NOT fix violations yet.

- [ ] **Step 3: Run ruff again to confirm D102 is active**

Run:
```bash
ruff check --select "D102" lib/iris --statistics
```

Expected: Same violations listed (rule is now active, not ignored).

- [ ] **Step 4: Fix all D102 violations**

For each violation, examine the method and add a docstring using NumPy style. If the method is a test helper, internal override, or intentionally undocumented, add `# noqa: D102` above the method definition instead.

**Decision rule:** Add a docstring unless the method is a known test helper, a simple override with documentation elsewhere, or explicitly internal. Document public methods, including `__init__`, `__repr__`, etc., unless they are trivial.

Use this template for `__init__`:

```python
def __init__(self, param1, param2):
    """
    Initialize ClassName.

    Parameters
    ----------
    param1 : type
        Description of param1.
    param2 : type
        Description of param2.
    """
```

For regular methods:

```python
def method_name(self, param1):
    """
    Brief description of what this method does.

    Parameters
    ----------
    param1 : type
        Description of param1.

    Returns
    -------
    return_type
        Description of return value.
    """
```

- [ ] **Step 5: Run pre-commit to validate docstrings and formatting**

Run:
```bash
pre-commit run --files lib/iris --all-files
```

Expected: All hooks pass, or return errors for invalid docstring format (fix immediately).

- [ ] **Step 6: Run ruff one more time to confirm zero D102 violations**

Run:
```bash
ruff check --select "D102" lib/iris --statistics
```

Expected: No violations reported.

- [ ] **Step 7: Commit**

Run:
```bash
git add pyproject.toml lib/iris
git commit -m "Enable ruff rule D102: missing docstring in public method

Add docstrings to <N> public methods to comply with D102.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

(Replace `<N>` with the count from Step 1.)

- [ ] **Step 8: Create a pull request**

Run:
```bash
gh pr create --title "Enable D102: missing docstring in public method" \
  --body "(posted by Claude Opus)

Enable the D102 pydocstyle rule and add docstrings to <N> public methods.

This is part of the ruff rule adoption plan to progressively enable ignored rules. See the spec: docs/superpowers/specs/2026-11-17-ruff-rule-adoption-design.md"
```

---

## Task 3: Enable D103 (Missing docstring in public function)

**Files:**
- Modify: `pyproject.toml:216–217` (remove `D103` from ignore list)
- Modify: Multiple function definitions in `lib/iris/` (add docstrings or `# noqa: D103`)
- Test: Run ruff checks and pre-commit validation

**Interfaces:**
- Consumes: Completed Task 2 (D102 rule enabled and all violations fixed); updated `pyproject.toml`
- Produces: Updated `pyproject.toml` with D103 enabled; all public functions either documented or explicitly exempted

**Steps:**

- [ ] **Step 1: Identify D103 violations**

Run:
```bash
ruff check --select "D103" lib/iris --statistics
```

Expected output: A list of files and line numbers with public functions missing docstrings, plus a count of violations. Record the count for the PR description.

- [ ] **Step 2: Enable D103 in pyproject.toml**

Edit `pyproject.toml` to remove the line:
```python
"D103",  # Missing docstring in public function
```

Save the file. Do NOT fix violations yet.

- [ ] **Step 3: Run ruff again to confirm D103 is active**

Run:
```bash
ruff check --select "D103" lib/iris --statistics
```

Expected: Same violations listed (rule is now active, not ignored).

- [ ] **Step 4: Fix all D103 violations**

For each violation, examine the function and add a docstring using NumPy style. If the function is a test helper or intentionally undocumented, add `# noqa: D103` above the function definition instead.

**Decision rule:** Add a docstring to all public module-level functions unless they are clearly test-scoped helpers (e.g., `_helper()` with leading underscore should not trigger D103, but public functions should be documented).

Use this template:

```python
def function_name(param1, param2):
    """
    Brief description of what this function does.

    Parameters
    ----------
    param1 : type
        Description of param1.
    param2 : type
        Description of param2.

    Returns
    -------
    return_type
        Description of return value.
    """
```

- [ ] **Step 5: Run pre-commit to validate docstrings and formatting**

Run:
```bash
pre-commit run --files lib/iris --all-files
```

Expected: All hooks pass, or return errors for invalid docstring format (fix immediately).

- [ ] **Step 6: Run ruff one more time to confirm zero D103 violations**

Run:
```bash
ruff check --select "D103" lib/iris --statistics
```

Expected: No violations reported.

- [ ] **Step 7: Commit**

Run:
```bash
git add pyproject.toml lib/iris
git commit -m "Enable ruff rule D103: missing docstring in public function

Add docstrings to <N> public functions to comply with D103.

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

(Replace `<N>` with the count from Step 1.)

- [ ] **Step 8: Create a pull request**

Run:
```bash
gh pr create --title "Enable D103: missing docstring in public function" \
  --body "(posted by Claude Opus)

Enable the D103 pydocstyle rule and add docstrings to <N> public functions.

This is part of the ruff rule adoption plan to progressively enable ignored rules. See the spec: docs/superpowers/specs/2026-11-17-ruff-rule-adoption-design.md"
```

---

## Checklist for Completion

- [ ] All three tasks completed and PRs merged
- [ ] `pyproject.toml` has D101, D102, D103 removed from ignore list
- [ ] All public classes documented (or explicitly exempted with `# noqa`)
- [ ] All public methods documented (or explicitly exempted with `# noqa`)
- [ ] All public functions documented (or explicitly exempted with `# noqa`)
- [ ] Pre-commit passes on all three rules
- [ ] `ruff check --select "D101,D102,D103" lib/iris` reports zero violations
- [ ] All PRs merged into `main`
- [ ] Spec updated with final roadmap and merge log

