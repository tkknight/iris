# Iris custom benchmarks

To be recognised by ASV, these benchmarks must be packaged and installed in 
line with the
[ASV guidelines](https://asv.readthedocs.io/projects/asv-runner/en/stable/development/benchmark_plugins.html).
This is achieved using the custom build in [install.py](./install.py).

Installation is into the environment where benchmarks are run, not the
Pixi environment used to invoke ASV. ASV selects a per-commit environment
from the Pixi workspace or a historical Conda lockfile. This is done via
`build_command` in [asv.conf.json](../asv.conf.json).
