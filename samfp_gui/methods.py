# -*- coding: utf-8 -*-


def calc_order(wavelength, gap_size):
    """
    Returns the FP interferential order.

    Parameters
    ----------
    wavelength (float):
    gap_size (float):

    Returns
    -------
    order (float)
    """
    try:
        foo = 2 * (gap_size * 1e-6) / (wavelength * 1e-10)
    except ZeroDivisionError as e:
        foo = -1
    return


def calc_finesse(fsr, fwhm):
    """
    Returns the FP Finesse.

    Parameters
    ----------
    FSR (float) : free-spectral-range in BCV or A
    FWHM (float) : full-width-at-half-maximum in BCV or A

    Returns
    -------
    F (float) : the finesse

    Observations
    ------------
    Both FSR and FWHM have to have same units.
    """
    try:
        foo = float(fsr) / float(fwhm)
    except ZeroDivisionError as e:
        foo = -1
    return foo


def calc_queensgate_constant(wavelength, free_spectra_range_bcv):
    """
    Returns the Fabry-Perot's Queensgate Constant.

    Parameters
    ----------
    wavelength (float):
    free_spectra_range_bcv (float):


    Returns
    -------
    queensgate_constant (float) :
    """
    try:
        foo = wavelength / free_spectra_range_bcv
    except ZeroDivisionError as e:
        foo = -1
    return foo
