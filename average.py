"""
Computes the average density value contained within an isosurface.

Assumes an orthorhombic cell.
"""
from argparse import ArgumentParser
from util.util import read_cube, compute_density, normalize, filter_density
from util.util import compute_volume
from numpy import where

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str,
                        help="the path to the file to process")
    parser.add_argument("norm", type=float, 
                        help="the normalization factor")
    parser.add_argument("iso_fract", type=float, 
                        help="the isosurface value cutoff as a fraction")

    args = parser.parse_args()

    # Read in the data.
    wf, spacing = read_cube(args.file)

    # Compute the density.
    p = compute_density(wf)
    normp = normalize(p, spacing, args.norm)

    # Filter to remove all but a certain percentage of the data.
    filtered = filter_density(normp, spacing, args.norm, args.iso_fract)

    # Compute the final values.
    sumval = compute_volume(filtered, spacing)
    mask = where(filtered > 0)

    # Print the averages.
    print("Average (Whole Domain):", sumval / filtered.size)
    print("Average (Iso-Surface Contained)", sumval / len(mask[0]))
    print("Size of the Isosurface (Fraction of Domain)", 
          len(mask[0])/filtered.size)
