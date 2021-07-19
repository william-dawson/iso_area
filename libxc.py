"""
Computes the exc of a system.

Example:
python libxc.py input.cube --exchange LDA_X --correlation LDA_C_PW

Functional list:
https://www.tddft.org/programs/libxc/functionals/

Assumes an orthorhombic cell.
"""
from argparse import ArgumentParser
from util.util import read_cube, compute_density
from util.util import apply_functional, compute_volume
from math import pi

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str,
                        help="the path to the file to process")
    parser.add_argument("--exchange", type=str, default=None,
                        help="the exchange functional")
    parser.add_argument("--correlation", type=str, default=None,
                        help="the correlation functional")

    args = parser.parse_args()

    # Read in the data.
    wf, spacing = read_cube(args.file)
    p = compute_density(wf)

    # Compute the exchange energy
    poly = apply_functional(p, args.exchange)
    sumval = compute_volume(poly, spacing)*(3/4)*(3/pi)**(1/3)

    # Compute the correlation energy
    poly = apply_functional(p, args.correlation)
    sumval += compute_volume(poly, spacing)

    # Compute the final values.
    print(sumval)
