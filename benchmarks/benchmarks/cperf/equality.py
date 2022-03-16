# Copyright Iris contributors
#
# This file is part of Iris and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.
"""
Equality benchmarks for the CPerf scheme of the UK Met Office's NG-VAT project.
"""
from . import SingleDiagnosticMixin
from .. import on_demand_benchmark


class EqualityMixin(SingleDiagnosticMixin):
    """
    Uses :class:`SingleDiagnosticMixin` as the realistic case will be comparing
    :class:`~iris.cube.Cube`\\ s that have been loaded from file.
    """

    # Cut down the parent parameters.
    params = [["LFRic", "UM"]]

    def setup(self, file_type, three_d=False, three_times=False):
        super().setup(file_type, three_d, three_times)
        self.cube = self.load()
        self.other_cube = self.load()


@on_demand_benchmark
class CubeEquality(EqualityMixin):
    """
    Benchmark time and memory costs of comparing LFRic and UM
     :class:`~iris.cube.Cube`\\ s.
    """

    def _comparison(self):
        _ = self.cube == self.other_cube

    def peakmem_eq(self, file_type):
        self._comparison()

    def time_eq(self, file_type):
        self._comparison()


@on_demand_benchmark
class MeshEquality(EqualityMixin):
    """Provides extra context for :class:`CubeEquality`."""

    params = [["LFRic"]]

    def _comparison(self):
        _ = self.cube.mesh == self.other_cube.mesh

    def peakmem_eq(self, file_type):
        self._comparison()

    def time_eq(self, file_type):
        self._comparison()
