import pytest
import numpy as np
from numpy.testing import assert_array_equal
from ..prior import UniformPrior, GaussianPrior, JointPrior


def test_uniform_prior():
    unif = UniformPrior(-.5, .5)
    x = np.array([-.25, .25, 0])

    assert np.isfinite(unif(x))
    assert not np.isfinite(unif(x + 1))

def test_add_uniform_priors():
    unif = UniformPrior(-.5, .5) + UniformPrior(.5, 1.)
    assert isinstance(unif, UniformPrior)
    assert np.isfinite(unif((.4999, .5)))
    assert ~np.isfinite(unif((.5, .5)))

    unif = unif + UniformPrior(2., 3.)
    assert isinstance(unif, UniformPrior)
    assert np.isfinite(unif((.4999, .5, 2.5)))
    assert ~np.isfinite(unif((.5, .5, .0)))

def test_gaussian_prior():
    gauss = GaussianPrior(0, 1)
    assert gauss(0) == 0.0
    assert gauss(4) == 8.0

def test_add_gaussian_priors():
    gauss = GaussianPrior(0, 1) + GaussianPrior(1, 1)
    assert gauss((0, 1)) == 0.0
    assert gauss((2, 3)) == 4.0

def test_joint_prior():
    unif = UniformPrior(-1, 1)
    gauss = GaussianPrior(0, 1)
    jp = JointPrior(unif, gauss)

    assert jp.evaluate((.5, .5)) == unif.evaluate(.5) + gauss.evaluate(.5)
    assert not np.isfinite(jp((1.5, .5)))

    jp = jp + jp
    assert jp.evaluate((.5, .5, .5, .5)) == 2 * (unif.evaluate(.5) + gauss.evaluate(.5))
    assert not np.isfinite(jp((1.5, 1.5, 1.5, 1.5)))
