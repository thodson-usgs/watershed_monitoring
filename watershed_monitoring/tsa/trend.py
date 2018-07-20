"""
Tests for trends in time series data

Nonparametric Trend Tests
-------------------------
Nonparametric tests should be used where one or more of the following
conditions exist in the data.

    1. The data are nonnormal.

    2. There are missing values in the data.

    3. The data are censored. Censored data are those observations report
    at as being less than or greater than some threshold value.

In some cases, it may be remove the affect of covariates from a trend test.
With such methods, the variable under consideration is adjusted by one or
several covariates by building a regression model and applying the trend test
to the residuals. A common example of this approach is flow-normalization,
which attempts to remove the effect of natural variablity in flow on the
concentration of a particular constituent in a stream.  Nonparametric
procedures cannot be applied to flow-adjusted records containing censored data
since regression residuals cannot be computed for censored values (Hirsch et
al., 1991).

References
----------
.. [1] Hirsch, R.M., R.B. Alexander, R.A. Smith. 1991. Selection of Methods
       for the Detection and Estimation of Trends in Water Quality Data.
       Water Resources Research.

Resources
----------
.. [1] https://up-rs-esp.github.io/mkt/#
.. [2] https://cran.r-project.org/web/packages/trend/vignettes/trend.pdf
"""

import pandas as pd
import numpy as np


from scipy.stats import mannwhitneyu, norm

def partial_mann_kendall(x,y):
    """Partial Mann-Kendall Trend Test

    A nonparametric test for a monotonic trend, which accounts for the influences of a covariate.

    Paramters
    ---------
    x : array
        A chronologically ordered sequence of observations.
    y : array
        Coincident observations of a covariate.

    Returns
    -------

    Note
    ----
    Does not yet account for ties.

    References
    ----------
    .. [1] Libiseller, C. and Grimvall, A., (2002). Performance of partial
    Mann-Kendall tests for trend detection in the presence of covariates.
    Environmetrics 13, 71--84, \url{http://dx.doi.org/10.1002/env.507}.

    Attribution
    -----------
    """

    # test that x and y are the same length

    # coumpute MK scores
    s_x = mk_score(x)
    s_y = mk_score(y)

def pmk_k(x,y):
    """Calculate the K term of the Partial Mann Kendall test.

    Parameters
    ----------
    x : array
    y : array

    Returns
    -------
    K term of the PMK test.
    """
    n = len(x)
    k = 0

    for i in np.arange(1:n-1):

def pmk_r(x):
    """Calculate the R term of the Partial Mann Kendall test.

    Parameters
    ----------
    x : array
        A chronologically ordered sequence of observations.

    Returns
    -------
    An array of R values used in determing conditional covariance.
    """
    n = len(x)
    r = np.zeroes_like(x)

    for j in np.arange(1,n):
        s = 0

        for i in np.arange(1,n):
            s += np.sum(np.sign(x[j] - x[i]))
            r[j] = (n+1+s)/2

    return r


def ar1_trend_correction(rho, n=None):
    """Coefficient to correct trend statistics for autocorrelation.

    Used to adjust the variance or standard deviation of the trend statistic in
    MDC or variaous trend tests.  Only appropriate for data exhibiting AR(1)
    structure, which is typical for water quality data collected at weekly,
    biweekly, or mothly intervals. Higher-frequency data should be tested for
    higher-order AR terms, and may require aggregation.

    To apply the correction, multiply the variance by coefficient, or mulitply
    the standard deviation by the square root of the coefficient.


    Parameters
    ----------
    rho : float
        Autocorrelation coefficient at lag 1.

    n : int
        Sample size. Can be ignored for large sample sizes.

    Returns
    -------
    Correction coefficient. Take the square root when used to correct standard deviation.


    References
    ----------
    .. [1] Spooner et al. 2011. Tech Notes 6: Statistical Analysis for Monotonic Trends.
           USEPA.
    .. [2] Fuller, W.A. 1976. Introduction to Statistical Time Series.
           John Wiley & Sons, Inc. New York.
    .. [3] Matalas, N.C. and W.B. Langbein. 1962. Information content of the mean.
           Journal of Geophysical Research 67(9):3441-34498
    """
    c = (1+rho)/(1-rho)

    if n is not None:
        # apply correction for sample size
        c -= (2/n)*(rho*(1-rho**n))/((1-rho)**2)

    return c


def mk_z(s, var_s):
    """Compoutes the MK test statistic, Z.

    Parameters
    ----------
    s : float
        The MK trend statistic, S.

    var_s : float
        Variance of S.

    Returns
    -------
    MK test statistic, Z.
    """
    #calculate the MK test statistic
    if s > 0:
        z = (s - 1)/np.sqrt(var_s)
    elif s < 0:
        z = (s + 1)/np.sqrt(var_s)
    else: # s == 0:
        z = 0

    return z


def mk_score(x):
    """Computes S statistic used in Mann-Kendall tests.

    Parameters
    ----------
    x : array_like
        Chronologically ordered array of observations.

    Returns
    -------
    MK trend statistic (S).

    Formula
    -------
	The MK statistic is defined as

		.. math::
			S = \sum_{i<j} (x_i - x_j)

	where
		..math::

			sgn(x_i - x_j) &=
            \begin{cases}
                        1,  & x_i - x_j > 0\\
                        0,  & x_i - x_j = 0\\
                        -1, & x_i - x_j < 0
            \end{cases},

	which tells us whether the difference between the measurements at time
	:math:`i` and :math:`j` are positive, negative or zero.
    """
    n = len(x)
    s = 0

    for j in np.arange(1,n):
        s += np.sum(np.sign(x[j] - x[0:j]))

    return s


def mk_score_variance(x):
    """Computes corrected variance of S statistic used in Mann-Kendall tests.

    Equation 8.4 from Helsel and Hirsch (2002). Also see XXX

    Parameters
    ----------
    x : array_like

    Returns
    -------
    Variance of S statistic

    Formula
    -------
    The variance :math:`Var(S)` is often given as:

        .. math::
            VAR(S) = \frac{1}{18} \Big( n(n-1)(2n+5) - \sum_{k=1}^p
            q_k(q_k-1)(2q_k+5) \Big),

    where :math:`p` is the total number of tie groups in the data, and :math:`q_k`
    is the number of data points contained in the :math:`k`-th tie group.

    Note that this might be equivalent to:

        See page 728 of Hirsch and Slack

    References
    ----------
    .. [1] Helsel and Hirsch, R.M. 2002. Statistical Methods in Water Resources.
    """
    n = len(x)
    # calculate the unique data
    unique_x = np.unique(x)
    # calculate the number of tied groups
    g = len(unique_x)

    # calculate the var(s)
    if n == g:  # there is no tie
        var_s = (n*(n-1)*(2*n+5))/18

    else:  # there are some ties in data
        tp = np.zeros_like(unique_x)
        for i in range(len(unique_x)):
            tp[i] = sum(x == unique_x[i])
        var_s = (n*(n-1)*(2*n+5) - np.sum(tp*(tp-1)*(2*tp+5)))/18

    return var_s


def kendall(x, alpha=0.05):
    """Mann-Kendall (MK) is a nonparametric test for monotonic trend.

    Parameters
    ----------
    x : array
    Data in the order it was collected in time.

    Returns
    -------
    z : float
        normalized MK test statistic.

    p : float

    Background
    ----------
    The purpose of the Mann-Kendall (MK) test (Mann 1945, Kendall 1975, Gilbert
    1987) is to statistically assess if there is a monotonic upward or downward
    trend of the variable of interest over time. A monotonic upward (downward)
    trend means that the variable consistently increases (decreases) through
    time, but the trend may or may not be linear. The MK test can be used in
    place of a parametric linear regression analysis, which can be used to test
    if the slope of the estimated linear regression line is different from
    zero. The regression analysis requires that the residuals from the fitted
    regression line be normally distributed; an assumption not required by the
    MK test, that is, the MK test is a non-parametric (distribution-free) test.

    Hirsch, Slack and Smith (1982, page 107) indicate that the MK test is best
    viewed as an exploratory analysis and is most appropriately used to
    identify stations where changes are significant or of large magnitude and
    to quantify these findings.

    Examples
    --------
    >>> x = np.random.rand(100) + np.linspace(0,.5,100)
    >>> z,p = kendall(x)

    References
    ----------

    Attribution
    -----------
    Background authored by Sat Kumar Tomer, available at
    https://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm

    Modified from code by Michael Schramn available at
    https://github.com/mps9506/Mann-Kendall-Trend/blob/master/mk_test.py
    """
    n = len(x)

    s = mk_score(x)
    var_s = mk_score_variance(x)

    z = mk_z(s, var_s)
    # calculate the p_value
    p = 2*(1-norm.cdf(abs(z)))  # two tail test

    return z, p

def seasonal_kendall(x, period=12):
    """ Seasonal nonparametric test for detecting a monotonic trend.

    Parameters
    ----------
    x : array
        A sequence of chronologically ordered observations with fixed
        frequency.

    period : int
        The number of observations that define period. This is the number of seasons.

    Background
    ----------
    The purpose of the Seasonal Kendall (SK) test (described in Hirsch, Slack
    and Smith 1982, Gilbert 1987, and Helsel and Hirsch 1995) is to test for a
    monotonic trend of the variable of interest when the data collected over
    time are expected to change in the same direction (up or down) for one or
    more seasons, e.g., months. A monotonic upward (downward) trend means that
    the variable consistently increases (decreases) over time, but the trend may
    or may not be linear. The presence of seasonality implies that the data have
    different distributions for different seasons (e.g., months) of the year.
    For example, a monotonic upward trend may exist over years for January but
    not for June.

    The SK test is an extension of the Mann-Kendall (MK) test. The MK test
    should be used when seasonality is not expected to be present or when trends
    occur in different directions (up or down) in different seasons. The SK test
    is a nonparametric (distribution-free) test, that is, it does not require
    that the data be normally distributed. Also, the test can be used when there
    are missing data and data less that one or more limits of detection (LD).

    The SK test was proposed by Hirsch, Slack and Smith (1982) for use with 12
    seasons (months). The SK test may also be used for other seasons, for
    example, the four quarters of the year, the three 8-hour periods of the day,
    and the 52 weeks of the year. Hirsch,
    Slack and Smith (1982) showed that it is appropriate to use the standard
    normal distribution to conduct the SK test for monthly data when there are 3
    or more years of monthly data. For any combination of seasons and years they
    also show how to determine the exact distribution of the SK test statistic
    rather than assume the exact distribution is a standard normal distribution.

    Assumptions
    -----------
    The following assumptions underlie the SK test:

    1. When no trend is present the observations are not serially correlated
    over time.

    2. The observations obtained over time are representative of the true
    conditions at sampling times.

    3. The sample collection, handling, and measurement methods provide
    unbiased and representative observations of the underlying populations
    over time.abs

    4. Any monotonic trends present are all in the same direction (up or
    down). If the trend is up in some seasons and down in other seasons, the
    SK test will be misleading.

    5. The standard normal distribution may be used to evaluate if the
    computed SK test statistic indicates the existence of a monotonic trend
    over time.

    There are no requirements that the measurements be normally distributed
    or that any monotonic trend, if present, is linear. Hirsch and Slack
    (1994) develop a modification of the SK test that can be used when
    serial correlation over time is present.

    References
    ----------
    Gilbert, R.O. 1987. Statistical Methods for Environmental Pollution
    Monitoring. Wiley, NY.

    Helsel, D.R. and R.M. Hirsch. 1995. Statistical Methods in Water Resources.
    Elsevier, NY.

    Hirsch, R.M. and J.R. Slack. 1984. A nonparametric trend test for seasonal
    data with serial dependence. Water Resources Research 20(6):727-732.

    Hirsch, R.M., J.R. Slack and R.A. Smith. 1982. Techniques of Trend Analysis
    for Monthly Water Quality Data. Water Resources Research 18(1):107-121.

    Attribution
    -----------
    Text copied from
    https://vsp.pnnl.gov/help/vsample/Design_Trend_Seasonal_Kendall.htm
    """
    # Compute the SK statistic, S, for each season
    s = np.zeros(period)
    for season in np.arange(period):
        x_season = x[period::period]
        s += mk_score(x)
        var_s += mk_score_variance(x)

    # Compute the SK test statistic, Z, for each season.
    z = mk_z(s, var_s)

    # calculate the p_value
    p = 2*(1-norm.cdf(abs(z)))  # two tail test

    return z, p


def seasonal_rank_sum():
    """Seasonal rank-sum test for detecting a step trend.

    Parameters
    ==========

    Background
    ==========
    The seasonal rank-sum test is an extension of the rank-sum test described in
    Helsel and Hirsch (1992). The rank-sum test is a nonparametric test to
    determine whether two independent sets of data are significantly different
    from one another.  The results of the test indicate the direction of the
    change from the first dataset to the second dataset (upward or downward) and
    the level of significance of this change.

    References
    ==========
    - https://pubs.usgs.gov/sir/2016/5176/sir20165176.pdf
    """
    pass

def rank_sum(x, y):
    """
    Rank-sum test described in Helsel and Hirsch (1992).

    In its most general form, the rank-sum test is a test for whether one group
    tends to produce larger observations than the second group.

    Parameters
    ----------
    group1 : series
    group2 : series

    Background
    ----------
    The rank-sum test goes by many names. It was developed by Wilcoxon (1945),
    and so is sometimes called the Wilcoxon rank-sum test. It is equivalent to a
    test developed by Mann and Whitney near the same time period, and the test
    statistics can be derived one from the other. Thus the Mann-Whitney test
    is another name for the same test. The combined name of
    Wilcoxon-Mann-Whitney rank-sum test has also been used.

    Nonparametric tests possess the very useful property of being invariant to
    power transformations such as those of the ladder of powers. Since only the
    data or any power transformation of the data need be similar except for
    their central location in order to use the rank-sum test, it is applicable
    in many situations.

    The exact form of the rank-sum test is given below. It is the only form
    appropriate for comparing groups of sample size 10 or smaller per group.
    When both groups have samples sizes greater than 10 (n, m > 10), the
    large-sample approximation may be used. Remember that computer packages
    report p-values from the large sample approximation regardless of sample
    size.

    References
    ----------
    .. [1] Helsel, D.R. and R.M. Hirsch. 1995. Statistical Methods in Water Resources.
    Elsevier, NY.

    Attribution
    -----------
    Text copied from Helsel and Hirsch 1995.
    """
    pass


def mannwhitney(x, y, use_continuity=True, alternative=None):
    """
    Compute the Mann-Whitney rank test on samples x and y.

    Parameters
    ----------
    x, y : array_like
        Array of samples, should be one-dimensional.
    use_continuity : bool, optional
            Whether a continuity correction (1/2.) should be taken into
            account. Default is True.
    alternative : None (deprecated), 'less', 'two-sided', or 'greater'
            Whether to get the p-value for the one-sided hypothesis ('less'
            or 'greater') or for the two-sided hypothesis ('two-sided').
            Defaults to None, which results in a p-value half the size of
            the 'two-sided' p-value and a different U statistic. The
            default behavior is not the same as using 'less' or 'greater':
            it only exists for backward compatibility and is deprecated.
    Returns
    -------
    statistic : float
        The Mann-Whitney U statistic, equal to min(U for x, U for y) if
        `alternative` is equal to None (deprecated; exists for backward
        compatibility), and U for y otherwise.
    pvalue : float
        p-value assuming an asymptotic normal distribution. One-sided or
        two-sided, depending on the choice of `alternative`.
    Notes
    -----
    Use only when the number of observation in each sample is > 20 and
    you have 2 independent samples of ranks. Mann-Whitney U is
    significant if the u-obtained is LESS THAN or equal to the critical
    value of U.
    This test corrects for ties and by default uses a continuity correction.
    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Mann-Whitney_U_test
    .. [2] H.B. Mann and D.R. Whitney, "On a Test of Whether one of Two Random
           Variables is Stochastically Larger than the Other," The Annals of
           Mathematical Statistics, vol. 18, no. 1, pp. 50-60, 1947.
    """
    mannwhitneyu(x,y, use_continuity, alternative)

def check_num_samples(beta, delta, std_dev, alpha=0.05, n=4, num_iter=1000,
                      tol=1e-6, num_cycles=10000, m=5):
    """
    This function is an implementation of the "Calculation of Number of Samples
    Required to Detect a Trend" section written by Sat Kumar Tomer
    (satkumartomer@gmail.com) which can be found at:
    http://vsp.pnnl.gov/help/Vsample/Design_Trend_Mann_Kendall.htm
    As stated on the webpage in the URL above the method uses a Monte-Carlo
    simulation to determine the required number of points in time, n, to take a
    measurement in order to detect a linear trend for specified small
    probabilities that the MK test will make decision errors. If a non-linear
    trend is actually present, then the value of n computed by VSP is only an
    approximation to the correct n. If non-detects are expected in the
    resulting data, then the value of n computed by VSP is only an
    approximation to the correct n, and this approximation will tend to be less
    accurate as the number of non-detects increases.

    Parameters
    ----------
        beta: probability of falsely accepting the null hypothesis
        delta: change per sample period, i.e., the change that occurs between
               two adjacent sampling times
        std_dev: standard deviation of the sample points.
        alpha: significance level (0.05 default)
        n: initial number of sample points (4 default).
        num_iter: number of iterations of the Monte-Carlo simulation (1000
                  default).
        tol: tolerance level to decide if the predicted probability is close
             enough to the required statistical power value (1e-6 default).
        num_cycles: Total number of cycles of the simulation. This is to ensure
                    that the simulation does finish regardless of convergence
                    or not (10000 default).
        m: if the tolerance is too small then the simulation could continue to
           cycle through the same sample numbers over and over. This parameter
           determines how many cycles to look back. If the same number of
           samples was been determined m cycles ago then the simulation will
           stop.
    Examples
    --------
        >>> num_samples = check_num_samples(0.2, 1, 0.1)
    """
    # Initialize the parameters
    power = 1.0 - beta
    P_d = 0.0
    cycle_num = 0
    min_diff_P_d_and_power = abs(P_d - power)
    best_P_d = P_d
    max_n = n
    min_n = n
    max_n_cycle = 1
    min_n_cycle = 1
    # Print information for user
    print("Delta (gradient): {}".format(delta))
    print("Standard deviation: {}".format(std_dev))
    print("Statistical power: {}".format(power))

    # Compute an estimate of probability of detecting a trend if the estimate
    # Is not close enough to the specified statistical power value or if the
    # number of iterations exceeds the number of defined cycles.
    while abs(P_d - power) > tol and cycle_num < num_cycles:
        cycle_num += 1
        print("Cycle Number: {}".format(cycle_num))
        count_of_trend_detections = 0

        # Perform MK test for random sample.
        for i in xrange(num_iter):
            r = np.random.normal(loc=0.0, scale=std_dev, size=n)
            x = r + delta * np.arange(n)
            trend, h, p, z = mk_test(x, alpha)
            if h:
                count_of_trend_detections += 1
        P_d = float(count_of_trend_detections) / num_iter

        # Determine if P_d is close to the power value.
        if abs(P_d - power) < tol:
            print("P_d: {}".format(P_d))
            print("{} samples are required".format(n))
            return n

        # Determine if the calculated probability is closest to the statistical
        # power.
        if min_diff_P_d_and_power > abs(P_d - power):
            min_diff_P_d_and_power = abs(P_d - power)
            best_P_d = P_d

        # Update max or min n.
        if n > max_n and abs(best_P_d - P_d) < tol:
            max_n = n
            max_n_cycle = cycle_num
        elif n < min_n and abs(best_P_d - P_d) < tol:
            min_n = n
            min_n_cycle = cycle_num

        # In case the tolerance is too small we'll stop the cycling when the
        # number of cycles, n, is cycling between the same values.
        elif (abs(max_n - n) == 0 and
              cycle_num - max_n_cycle >= m or
              abs(min_n - n) == 0 and
              cycle_num - min_n_cycle >= m):
            print("Number of samples required has converged.")
            print("P_d: {}".format(P_d))
            print("Approximately {} samples are required".format(n))
            return n

        # Determine whether to increase or decrease the number of samples.
        if P_d < power:
            n += 1
            print("P_d: {}".format(P_d))
            print("Increasing n to {}".format(n))
            print("")
        else:
            n -= 1
            print("P_d: {}".format(P_d))
            print("Decreasing n to {}".format(n))
            print("")
            if n == 0:
                raise ValueError("Number of samples = 0. This should not happen.")