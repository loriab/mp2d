"""
Unit and regression test for the mp2d package.
"""

# Import package, test suite, and other packages as needed
import mp2d
import pytest
import sys

def test_mp2d_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "mp2d" in sys.modules

def test_fromstr():
    seneyne = """
C   0.000000  -0.667578  -2.124659
C   0.000000   0.667578  -2.124659
H   0.923621  -1.232253  -2.126185
H  -0.923621  -1.232253  -2.126185
H  -0.923621   1.232253  -2.126185
H   0.923621   1.232253  -2.126185
--
C   0.000000   0.000000   2.900503
C   0.000000   0.000000   1.693240
H   0.000000   0.000000   0.627352
H   0.000000   0.000000   3.963929
"""

    ans = mp2d.run_json(seneyne)
    assert ans['energy'] == pytest.approx(4.0)
    #assert 0  # if you ever need test to fail so you can see printing

def test_badelement_error():
    she = """He 0 0 0\nKr 1 0 0 """

    with pytest.raises(mp2d.DataUnavailableError):
        mp2d.run_json(she)
