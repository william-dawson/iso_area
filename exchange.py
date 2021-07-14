"""
Computes the exchange enrgy of the density: 
\sum f(p(r))dr where $f$ is the lda exchange.

Assumes an orthorhombic cell.
"""
from argparse import ArgumentParser
from util.util import read_cube, compute_density
from util.util import apply_polynomial, compute_volume
from math import pi

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str,
                        help="the path to the file to process")

    args = parser.parse_args()

    # Read in the data.
    wf, spacing = read_cube(args.file)
    p = compute_density(wf)
    poly = apply_polynomial(p, "x**(4/3)")

    # Compute the final values.
    sumval = compute_volume(poly, spacing)

    print(sumval*-(3/4)*(3/pi)**(1/3))
