"""
mp2d.py
Dispersion correction for MP2

Handles the primary functions
"""
import math

import numpy as np
import qcelemental as qcel

from .exceptions import DataUnavailableError

def canvas(with_attribution=True):
    """
    Placeholder function to show example docstring (NumPy format)

    Replace this function and doc string for your own project

    Parameters
    ----------
    with_attribution : bool, Optional, default: True
        Set whether or not to display who the quote is from

    Returns
    -------
    quote : str
        Compiled string including quote and optional attribution
    """

    quote = "The code is but a canvas to our imagination."
    if with_attribution:
        quote += "\n\t- Adapted from Henry David Thoreau"
    return quote


def run_mp2d(geometry, symbols, a1=0.944, a2=0.480, rcut=0.72, width=0.20, s8=1.187):
    """

    Parameters
    ----------
    geometry : array-like
        Flat (3 * nat, ) or stout (nat, 3) list or ndarray of system geometry in Bohr [a0].
    symbols : array-like
        (nat, ) list or ndarray of system element symbols.
    a1 : float, optional
        Parameter (dimensionless) to control Tang-Toennies damping in the noncovalent regime.
    a2 : float, optional
        Parameter [AA] to control Tang-Toennies damping in the noncovalent regime
    rcut : float, optional
        Parameter (dimensionless) to control frontier between covalent and noncovalent regimes.
    width : float, optional
        Parameter (dimensionless) to control frontier between covalent and noncovalent regimes.
    s8 : float, optional
        Parameter (dimensionless) to control Tang-Toennies 8th order damping in the noncovalent regime.
        (6th order is fixed at 1.)

    """
    geometry = np.array(geometry).reshape(-1, 3)
    symbols = np.array(symbols)


    # some useful python calls
    math.factorial(4)
    qcel.periodictable.to_Z('P')
    qcel.constants.conversion_factor('bohr', 'angstrom')
    qcel.constants.conversion_factor('hartree', 'kcal/mol')
    qcel.covalentradii.get('P', units='bohr')

    from .data import GrimmeC6

    geom = np.arange(12, dtype=np.float64).reshape(-1, 3)
    nat = geom.shape[0]
    print(geom)
    dmat = qcel.util.distance_matrix(geom, geom)
    print(dmat)

    # CHECK THAT I DIDN'T MISCOUNT
    multipole_expectation_values = {
        'H': 8.0589,
        'B': 11.8799,
        'C': 7.8715,
        'N': 5.5588,
        'O': 4.7566,
        'F': 3.8025,
        'Ne': 3.1036,
        'P': 9.5361,
        'S': 8.1652,
        'Cl': 6.7463,
        'Ar': 5.6004,
        'Br': 7.1251
    }

    #if not set(symbols).issubset(multipole_expectation_values.keys()):
    un_mp2d_able_atoms = set(symbols).difference(multipole_expectation_values.keys())
    if un_mp2d_able_atoms:
        raise DataUnavailableError('multipole expectation value', str(un_mp2d_able_atoms))

    # some guidelines
    # * work entirely in atomic units -- input and output.
    # * if need external values (e.g., Multipole expectation values),
    #   copy them in in published units, notate the units, then convert
    #   immediately to atomic units.
    # * really need specialized mixed covalent radii (below) rather than just r0[H] + r0[B]?
    #
    #       void Coord_Num::GetCutoffRadii() {
    #
    #           // an array that contains the r0AB values for pairs of atoms.
    #           // For example, CovalentRadii[1][1] is the r0AB for HH.
    #           // CovalentRadii[1][5] is the r0AB for HB.
    #           double CutoffRadii[36][36] = {
    #               0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
    #
    # * if you're tempted to parse a molecule file, stop and ping me. I probably have an easier way. :-)
    # * the below is what's constraining elements, right?
    #
    #       double MultipoleExpectationValues[36] = { 0.0, 8.0589, 0.0, 0.0, 0.0, 11.8799, 7.8715, 5.5588, 4.7566, 3.8025
    #           ,3.1036, 0.0, 0.0, 0.0, 0.0, 9.5361, 8.1652, 6.7463, 5.6004, 0.0 ,0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.1251};
    #
    # * need to know number of fragments?

    return {'energy': 4.0,
            'gradient': np.zeros(nat * 3)}

def run_json(smol, a1=0.944, a2=0.480, rcut=0.72, width=0.20, s8=1.187):
    lab_molrec = qcel.molparse.from_string(smol)['qm']
    molssi_molrec = qcel.molparse.to_schema(lab_molrec, dtype=1)['molecule']
    # fields defined https://molssi-qc-schema.readthedocs.io/en/latest/auto_topology.html
    print(molssi_molrec)

    ans = run_mp2d(geometry=molssi_molrec['geometry'],
                   symbols=molssi_molrec['symbols'],
                   a1=a1,
                   a2=a2,
                   rcut=rcut,
                   width=width,
                   s8=s8)

    return ans

if __name__ == "__main__":
    # Do something if this file is invoked on its own
    print(canvas())
