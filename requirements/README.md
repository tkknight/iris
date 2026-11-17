Development and CI environments are defined in the root `pyproject.toml`
using Pixi. The committed `pixi.lock` records resolved dependencies; use
`pixi update` to refresh it. The scheduled lock workflow opens a pull request
when the lock changes.

`pypi-core.txt` remains the source of runtime dependencies declared for the
[scitools-iris](https://pypi.org/project/scitools-iris/) distribution. The
Read the Docs environment remains defined in `readthedocs.yml`.

