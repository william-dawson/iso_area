"""
Computes a function of the density: \sum f(p(r))dr where $f$ is a polynomial.

Assumes an orthorhombic cell.
"""
from argparse import ArgumentParser
try:
    from skimage.measure import marching_cubes
except ImportError:
    raise Exception("You need to install scikit-image")
from util.util import read_cube, compute_density, normalize, filter_density
from util.util import apply_polynomial, compute_volume, visualize


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str,
                        help="the path to the file to process")
    parser.add_argument("norm", type=float, 
                        help="the normalization factor")
    parser.add_argument("iso_fract", type=float, 
                        help="the isosurface value cutoff as a fraction")
    parser.add_argument("exponent", type=str, 
                        help="the exponent to use for the polynomial")
    parser.add_argument("--visualize", type=bool, required=False,
                        default=False,
                        help="If True, a picture of the isosurface is " +
                             "generated.")
    args = parser.parse_args()

    # Read in the data.
    wf, spacing = read_cube(args.file)

    # Compute the density.
    p = compute_density(wf)
    normp = normalize(p, spacing, args.norm)

    # Filter to remove all but a certain percentage of the data.
    filtered = filter_density(normp, spacing, args.norm, args.iso_fract)
    filtered_volume = compute_volume(filtered, spacing)

    # Apply the polynomial.
    poly = apply_polynomial(filtered, args.exponent)

    # Compute the final values.
    sumval = compute_volume(poly, spacing)

    # Print the results.
    print("Filtered Volume:", filtered_volume)
    print("Sum:", sumval)
    print("Average (Whole Domain):", sumval / poly.size)

    npts = 0
    for i in range(filtered.shape[0]):
        for j in range(filtered.shape[1]):
            for k in range(filtered.shape[2]):
                if filtered[i, j, k] > 0:
                    npts += 1
    print("Average (Inside Surface):", sumval / npts)

    # Visualize.
    if args.visualize:
        verts, faces, _, _ = marching_cubes(poly, level=1e-10,
                                            spacing=spacing)
        visualize(verts, faces, poly.shape, spacing)
