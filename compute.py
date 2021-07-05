"""
Compute the surface area of the data in a gaussian cubefile.

Assumes an orthorhombic cell.
"""
from argparse import ArgumentParser
try:
    from skimage.measure import marching_cubes
except ImportError:
    raise Exception("You need to install scikit-image")


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
                    data[i, j, k] = float(split[0])
                    split = split[1:]

    return data, spacing


def compute_isosurface_area(verts, faces):
    """
    Computes the surface area of a triangulated surface.

    Args:
        verts (list): list of vertices.
        faces (list): list of points defining the triangles.
    Returns:
        (float): the surface area.
    """
    from numpy import cross
    from numpy.linalg import norm
    total = 0
    for f in faces:
        v = verts[f[1]] - verts[f[0]]
        u = verts[f[2]] - verts[f[0]]
        total += 0.5*norm(cross(v, u))
    return total


def compute_volume(data, level, spacing):
    """
    Compute the volume of the isosurface.

    Args:
        data (list): the 3d underlying data.
        level (float): the isosurface level.
        spacing (list): the grid spacing.

    Returns:
        (float): the volume.
    """
    volume = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                if level > 0:
                    if data[i, j, k] > level:
                        volume += spacing[0]*spacing[1]*spacing[2]
                else:
                    if data[i, j, k] < level:
                        volume += spacing[0]*spacing[1]*spacing[2]

    return volume


def visualize(verts, faces, grid_points, spacing, level):
    """
    Visualize an isosurface.

    Args:
        verts (list): list of vertices.
        faces (list): list of points defining the triangles.
        grid_points (list): the data.
        spacing (list): the grid spacing.
        level (float): the isosurface level.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    triangles = []
    for f in faces:
        tri = (verts[f[0]], verts[f[1]], verts[f[2]])
        triangles.append(tri)

    axs = plt.subplot(projection="3d")

    if level > 0:
        color = "blue"
    else:
        color = "red"
    col = Poly3DCollection(triangles, color=color)
    axs.add_collection(col)

    axs.set_xlim([0, grid_points[0]*spacing[0]])
    axs.set_ylim([0, grid_points[1]*spacing[1]])
    axs.set_zlim([0, grid_points[2]*spacing[2]])

    plt.show()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str,
                        help="the path to the file to process")
    parser.add_argument("iso_value", type=float, 
                        help="the isosurface value cutoff")
    parser.add_argument("--visualize", type=bool, required=False,
                        default=False,
                        help="If True, a picture of the isosurface is " +
                             "generated.")
    args = parser.parse_args()

    # Read in the data.
    data, spacing = read_cube(args.file)

    # Compute the iso-surface.
    verts, faces, _, _ = marching_cubes(data, level=args.iso_value,
                                        spacing=spacing)

    # Compute the surface area.
    area = compute_isosurface_area(verts, faces)
    print("Surface Area:", area)

    # Compute the volume.
    volume = compute_volume(data, level=args.iso_value, spacing=spacing)
    print("Volume:", volume)

    # Optional visualization
    if args.visualize:
        visualize(verts, faces, data.shape, spacing, args.iso_value)
