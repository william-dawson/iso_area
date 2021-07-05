"""
Compute the surface area of the data in a gaussian cubefile.

Assumes an orthorhombic cell.
"""
from argparse import ArgumentParser


def read_cube(fname):
    """
    Read in a cube file.

    Args:
        fname (str): the path to the file to read.
    Result:
        (list, list): the data (3d array) and the spacing (1d array)
    """
    from numpy import zeros
    grid_points = []
    spacing = []

    with open(fname) as ifile:
        next(ifile)
        next(ifile)
        split = next(ifile).split()
        natoms = abs(int(split[0]))
        for i in range(3):
            split = next(ifile).split()
            grid_points.append(int(split[0]))
            spacing.append(float(split[i+1]))
            
        data = zeros(grid_points)
        for i in range(natoms):
            next(ifile)
        next(ifile)
        split = next(ifile).split()
        for i in range(grid_points[0]):
            for j in range(grid_points[1]):
                for k in range(grid_points[2]):
                    if len(split) == 0:
                        split = next(ifile).split()
                    data[i, j, k] = float(split[0])**2
                    split = split[1:]

    return data, spacing


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str,
                        help="the path to the file to process")
    args = parser.parse_args()

    # Read in the data.
    data, spacing = read_cube(args.file)

    print(data.mean())
