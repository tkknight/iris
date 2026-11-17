# Ruff Rule Adoption: Pydocstyle D101, D102, D103

> **This is a living document.** §6 is the single progress record for this
> programme — PR states, blockers, and decisions. Update §6 as work lands; do
> not track status anywhere else. The table below is a summary of §6.1 and
> nothing more.

| | |
|---|---|
| **Phase** | Planning |
| **Progress** | Spec and implementation plan complete; ready for execution. |
| **Next action** | Execute Task 1 (enable D101). |
| **Blocked on** | Nothing |
| **Branch** | Will be feature branches per rule (d101-adoption, d102-adoption, d103-adoption) |
| **Delivery** | Three pull requests, one per rule, into `main` |
| **Resolves** | Partial enablement of ignored ruff rules; sets pattern for future rule adoption. |

**Created:** 2026-11-17 · **Last updated:** 2026-11-17  
**Baseline:** `main` at HEAD  
**Python versions:** 3.12, 3.13, 3.14  
**Ruff version:** As defined in `pyproject.toml` (0.6.x+)

---

## 1. Summary

This spec defines the adoption of three pydocstyle rules (`D101`, `D102`,
`D103`) currently ignored in [pyproject.toml](/pyproject.toml). These rules
enforce docstrings on public classes, methods, and functions—a core part of
Iris's documentation standards.

The work is structured as three pull requests, one per rule, delivered
sequentially. Each PR enables the rule, fixes all violations, and validates
compliance with NumPy docstring standards and pre-commit checks. The rules are
currently marked "temporary" in the config; this work reclassifies them as
active enforcement.

---

## 2. What exists today

### 2.1 Ignored rules in `pyproject.toml`

Lines 211–225 of [pyproject.toml](/pyproject.toml) list exceptions marked
"TODO: Temporary checks to ignore, will be reviewed at a later date":

- **D101** – Missing docstring in public class
- **D102** – Missing docstring in public method  
- **D103** – Missing docstring in public function

Each rule is commented with a pointer to the pydocstyle documentation.

### 2.2 Docstring standards

Iris enforces **NumPy docstring style** via pre-commit hooks and pydocstyle
configuration. Every new docstring must follow the format specified in
[NumPy's docstring conventions](https://numpydoc.readthedocs.io/en/latest/format.html).
Key sections:

- **One-line summary** — Brief description, imperative mood
- **Extended summary** (optional) — Longer explanation
- **Parameters** — Argument names, types, descriptions
- **Returns** — Return type, name, description
- **Raises** — Exceptions the function may raise
- **Notes**, **Examples**, **References** (optional)

Pre-commit runs `pydocstyle` and `ruff check` on staged files; both must pass
before commit.

### 2.3 Current state of violations

The three rules remain ignored because fixing all violations at once is
time-consuming. This spec addresses that by adopting one rule at a time, with
all violations fixed in a single PR per rule, committed and merged before the
next rule is enabled.

**Estimated violation counts (before execution):**
- D101: Likely 50–150 public classes
- D102: Likely 100–300 public methods
- D103: Likely 100–200 public functions

(Exact counts obtained by running `ruff check --select "D10x" lib/iris
--statistics` per rule.)

---

## 3. What we're building

### 3.1 Outcomes

**At the end of this work:**

1. D101, D102, and D103 rules are **enabled** in `pyproject.toml`.
2. All public classes, methods, and functions in `lib/iris/` have
   docstrings following NumPy style, **or** are explicitly exempted with
   `# noqa: D10x` where documented as intentional.
3. Three PRs are merged into `main`, one per rule, with clean history and
   passing CI.
4. The workflow and decision patterns are documented for future rule
   adoptions.

### 3.2 Scope and non-goals

**In scope:**
- Enable D101, D102, D103 rules
- Fix all violations in `lib/iris/` (the main library code)
- Validate with pre-commit, ruff, and pytest
- Commit and PR per rule

**Out of scope:**
- Adopting other ignored rules (F, E, W, C90, N, UP, ANN, etc.) — handled
  in future batches
- Changing pre-commit hook configuration
- Restructuring existing docstrings (fix-only: add missing docstrings, do
  not rewrite existing ones)
- Writing exhaustive docstrings for internal/private code (D101/D102/D103
  apply to public APIs only)

### 3.3 Constraints

- **Backward compatibility:** No breaking API changes. Only docstrings are
  added; function/method signatures remain unchanged.
- **Python versions:** Code must remain compatible with 3.12, 3.13, 3.14.
- **Docstring style:** All new docstrings must follow NumPy style; pre-commit
  validation enforces this.
- **Line length:** 88 characters (Ruff/Black default), enforced by
  `ruff format`.
- **No unrelated changes:** Each PR fixes violations for one rule only. Do
  not refactor, reformat, or change unrelated code.

---

## 4. Design and decision log

### 4.1 Why these three rules first?

**D101, D102, D103** are the most focused pydocstyle rules and are already
tagged in `pyproject.toml` as temporary. They have clear, well-understood
violation patterns:

- **D101** (class docstrings) – Classes are top-level, bounded scope, and
  relatively few (~50–150). Adding docstrings is straightforward.
- **D102** (method docstrings) – More numerous (~100–300) but still tractable.
  Each has a clear receiver (the object instance).
- **D103** (function docstrings) – Largest (~100–200), but the most common
  public API surface and highest value.

This sequence validates the workflow with quick wins before tackling larger
rule families.

### 4.2 Why one PR per rule?

**Single rule per PR** ensures:

- **Reviewability** – Each PR is focused; reviewers can verify all docstrings
  for one rule without context-switching.
- **Independent merge** – Each rule can be reviewed and merged separately; if
  one PR requires changes, others are not blocked.
- **Clear history** – Git history clearly shows which violations were fixed
  for which rule, aiding debugging and rollback if needed.
- **CI stability** – Smaller PRs reduce the chance of CI flakes.

### 4.3 Why fix all violations at once per rule?

**All violations fixed in one cycle per rule** ensures:

- **Clean state** – After each PR merges, the rule is 100% compliant; no
  backlog of unfixed violations.
- **No partial enforcement** – Developers do not see inconsistent enforcement
  (e.g., some D101 violations allowed, others not).
- **Momentum** – Fixing violations in one shot is more efficient than
  trickling fixes across multiple PRs.

### 4.4 Docstring quality vs. quantity

**Decision:** When a public class/method/function lacks a docstring, the
implementer writes one that accurately describes its purpose and behavior.
If the purpose is unclear or the code is underdocumented, a placeholder
docstring is acceptable as a starting point; it will be refined in future
reviews.

**Exception:** Test files are excluded by pydocstyle defaults (`tests/` is
configured to ignore D10x rules). If a test violation appears, the
implementer checks the per-file-ignores config.

### 4.5 Legitimate suppression with `# noqa: D10x`

**Decision:** Use `# noqa: D10x` only for public classes/methods/functions
that are intentionally undocumented. Examples:

- A public method that overrides a parent's method (the parent's docstring
  applies).
- A trivial `__repr__` or `__str__` method (behavior is obvious).
- A wrapper that delegates directly to another documented function (the
  wrapped function's docstring is the primary reference).

Document the reason for suppression in a comment if it is non-obvious.

**Example:**

```python
def __repr__(self):  # noqa: D102
    return f"{self.__class__.__name__}({self._value!r})"
```

---

## 5. Implementation approach

### 5.1 Three-task workflow

Each rule gets one task in the implementation plan (`docs/superpowers/plans/`):

1. **Task 1: Enable D101** – Remove `D101` from ignore list, fix all public
   class docstrings, commit, create PR.
2. **Task 2: Enable D102** – Remove `D102` from ignore list, fix all public
   method docstrings, commit, create PR.
3. **Task 3: Enable D103** – Remove `D103` from ignore list, fix all public
   function docstrings, commit, create PR.

### 5.2 Per-rule steps

Each task follows this sequence:

1. **Enumerate violations** – Run `ruff check --select "D10x" lib/iris
   --statistics`
2. **Enable the rule** – Remove it from `pyproject.toml`'s `ignore` list
3. **Fix violations** – Add docstrings (or suppress with `# noqa`)
4. **Validate** – Run pre-commit, ruff, pytest
5. **Commit** – With message `"Enable ruff rule D10x: <description>"`
6. **Create PR** – With concise title and body

### 5.3 Docstring templates

**For classes:**

```python
class ClassName:
    """
    Brief one-line description.

    Optional longer description explaining purpose, usage, or relationship
    to other classes.
    """
```

**For methods (including `__init__`):**

```python
def method_name(self, param1, param2):
    """
    Brief description of what this method does.

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

**For functions:**

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

---

## 6. Progress and decisions

### 6.1 Roadmap

| Task | Rule | Status | PR | Notes |
|------|------|--------|-----|-------|
| 1    | D101 | Planned | — | Enable class docstrings |
| 2    | D102 | Planned | — | Enable method docstrings |
| 3    | D103 | Planned | — | Enable function docstrings |

### 6.2 Known issues and open questions

**None at spec stage.** Issues and decisions will be recorded here as work
progresses.

### 6.3 Decisions made

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-11-17 | Adopt D101, D102, D103 sequentially | Focused scope, well-understood rules, quick wins |
| 2026-11-17 | One PR per rule, all violations fixed | Clean state, reviewable, independent merge |
| 2026-11-17 | NumPy docstring style required | Already enforced by pre-commit; consistency |

### 6.4 Closed issues

(None yet.)

### 6.5 Merge log

(To be populated as PRs merge.)

| Rule | PR | Merged | Commit |
|------|-----|--------|--------|
| D101 | #— | — | — |
| D102 | #— | — | — |
| D103 | #— | — | — |

### 6.6 Change log

**2026-11-17** – Spec created; plan written; ready for execution.

---

## 7. Appendix: Ruff rule references

- [D101 – Missing docstring in public
  class](https://docs.astral.sh/ruff/rules/#pydocstyle-d)
- [D102 – Missing docstring in public
  method](https://docs.astral.sh/ruff/rules/#pydocstyle-d)
- [D103 – Missing docstring in public
  function](https://docs.astral.sh/ruff/rules/#pydocstyle-d)

**NumPy docstring guide:**
[numpydoc.readthedocs.io](https://numpydoc.readthedocs.io/en/latest/format.html)

**Iris docstring guidelines:**
[lib/iris/AGENTS.md](/lib/iris/AGENTS.md) – "Docstrings" section

---

## 8. Related issues and PRs

(To be linked as work progresses.)

- **Issue:** None yet
- **Blocking:** None
- **Blocked by:** None

