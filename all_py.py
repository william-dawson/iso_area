"""
Compute the ionization potentials of some molecules.
"""

# Convert Hartree to eV
_h_to_ev = 27.2114


def get_system(fname, basis):
    """
    Setup the system.

    Args:
        fname (str): file name
        basis (str): the basis set name

    Returns:
        (pyscf.GTO.Mole): the starting system.
    """
    from pyscf import gto
    sys = gto.Mole()
    sys.atom = fname
    sys.basis = basis
    return sys.build()


def get_cation(sys):
    """
    Get the system with one electron removed.

    Args:
        sys (pyscf.GTO.Mole): the starting system.

    Returns:
        (pyscf.GTO.Mole): the cation version of the system.
    """
    sys_p = sys.copy()
    sys_p.charge = 1
    sys_p.spin = 1
    return sys_p.build()


def compute_scaling(sys, mo):
    """
    Compute the LDA type scaling factor for an orbital.

    Args:
        sys (pyscf.GTO.Mole): the starting system.
        mo (array): a single molecular orbital

    Returns:
        (float): the scaling factor.
    """
    from pyscf import dft
    from numpy import outer

    # Create the grid
    ni = dft.numint.NumInt()
    grids = dft.gen_grid.Grids(sys)
    grids.level = 4
    grids.build()

    # Integrate
    dm = outer(mo, mo)
    _, exc, _ = ni.nr_rks(sys, grids, 'lda,', dm)
    return exc


if __name__ == "__main__":
    from sys import argv
    from pyscf import dft
    try:
        fname = argv[1]
        basis = argv[2]
    except IndexError:
        print("Parameter is 1) xyz file ; 2) basis set.")
        quit(1)

    # Setup the systems
    sys = get_system(fname, basis)
    sys_p = get_cation(sys)
    nocc = int(sys.nelectron / 2)

    # Compute the HOMO/LUMO
    print("Computing Molecule...")
    mf = dft.RKS(sys)
    mf.xc = "BLYP"
    mf.verbose = 0
    _ = mf.kernel()
    estimate_dft = (_h_to_ev * mf.mo_energy[nocc-1])

    print("Computing Cation...")
    mf_p = dft.UKS(sys_p)
    mf_p.xc = "BLYP"
    mf_p.verbose = 0
    _ = mf_p.kernel()
    estimate_p = _h_to_ev * mf_p.mo_energy[1, nocc - 1]

    # The starting correction
    print("Correction...")
    combined = estimate_dft + 0.5 * (estimate_p - estimate_dft)
    correction = combined - estimate_dft

    # Compute the scaling for the improved correction
    scaling = []
    for i in range(nocc):
        scaling.append(compute_scaling(sys, mf.mo_coeff[:, i]))

    result = [-1 * (_h_to_ev * x + scaling[i]/scaling[-1] * correction)
              for i, x in enumerate(mf.mo_energy[:nocc])]

    print("Delta SCF", -1 * _h_to_ev * (mf.e_tot - mf_p.e_tot))
    print("Orbital (+)", -1 * estimate_p)
    print("Orbital (neutral)", -1 * estimate_dft)
    print("Orbital (avg)", -1 * combined)
    print("All orbitals:")
    print(result)
