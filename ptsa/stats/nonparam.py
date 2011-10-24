#emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
#ex: set sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See the COPYING file distributed along with the PTSA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##

# global imports
import numpy as np
from scipy.stats import ttest_ind, ttest_1samp, norm


def ttest_ind_z_one_sided(X,Y):
    # do the test
    t,p = ttest_ind(X,Y)

    # convert the pvals to one-sided tests based on the t
    p = p/2.
    p[t>0] = 1-p[t<0]

    # convert the p to a z
    z = norm.ppf(p)
    
    return z


def permutation_test(X, Y=None, parametric=True, iterations=1000):
    """
    Perform a permutation test on paired or non-paired data.

    Observations must be on the first axis.
    """
    # see if paired or not and concat data
    if Y is None:
        paired = True
        data = X
        nX = len(X)
    else:
        paired = False
        data = np.r_[X,Y]
        nX = len(X)
        nY = len(Y)

    # currently no non-parametric
    if not parametric:
        raise NotImplementedError("Currently only parametric stats are supported.")

    # perform stats
    z_boot = []
    if paired:
        # paired stat
        raise NotImplementedError("Currently only non-paired stats are supported.")
        # first on actual data
        #t,p = ttest_1samp(data)
    else:
        # non-paired
        # first on actual data
        z = ttest_ind_z_one_sided(data[:nX],data[nX:])

        # now on random shuffles
        for i in xrange(iterations):
            # shuffle it
            np.random.shuffle(data)
            z_boot.append(ttest_ind_z_one_sided(data[:nX],data[nX:]))

    # convert z_boot to array
    z_boot = np.asarray(z_boot)

    # return those z values
    return z, z_boot
