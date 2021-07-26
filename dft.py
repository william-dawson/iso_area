"""
Computes the exc of a system.

Example:
python dft.py wavefunction.cube density.cube
  --exchange LDA_X --correlation LDA_C_PW

Functional list:
https://www.tddft.org/programs/libxc/functionals/

Assumes an orthorhombic cell.
"""
from argparse import ArgumentParser
from util.util import read_cube, compute_potential, compute_density
from util.util import compute_volume
from numpy import multiply
from math import pi

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("wavefunction", type=str,
                        help="the path to the wavefunction file to process")
    parser.add_argument("density", type=str,
                        help="the path to the density file to process")
    parser.add_argument("--exchange", type=str, default=None,
                        help="the exchange functional")
    parser.add_argument("--correlation", type=str, default=None,
                        help="the correlation functional")

    args = parser.parse_args()

    # Read in the data.
    wf, spacing = read_cube(args.wavefunction)
    p, spacing = read_cube(args.density)
    wf = compute_density(wf)

    # Compute the exchange potential
    ex_potential = compute_potential(p, args.exchange)*(3/4)*(3/pi)**(1/3)
    cor_potential = compute_potential(p, args.correlation)
    potential = ex_potential + cor_potential

    sumval = compute_volume(multiply(wf, potential), spacing)

    # Compute the final values.
    print(sumval)
