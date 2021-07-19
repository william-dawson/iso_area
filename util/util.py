"""
Utility functions.
"""


def apply_functional(data, fname):
    if fname is None:
        return 0 * data
    import pylibxc
    from numpy import reshape, multiply
    func = pylibxc.LibXCFunctional(fname, "unpolarized")
    val = func.compute({"rho": data})
    return multiply(reshape(val["vrho"], data.shape), data)


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


def compute_density(data):
    """
    Computes the density from the wavefunction data (i.e. squares each value).
    """
    from numpy import square
    return square(data)


def normalize(data, spacing, norm):
    """
    Normalizes the data to integrate to the norm value.

    Args:
        data (list): a 3d array of data.
        spacing (list): grid spacing of the data.
        norm (float): the value to normalize to.
    """
    volume = compute_volume(data, spacing)
    return data * norm/volume


def filter_density(data, spacing, norm, fraction):
    """
    Filter the data to zero such that only a give fraction remains.

    We'll try this with a sorted dictionary, which is the most naive way,
    but could be fast enough.

    Args:
        data (list): a 3d array of data.
        spacing (list): grid spacing of the data.
        mnorm (float): the norm value of the data.
        fraction (float): the fraction to filter out.
    """
    from copy import deepcopy
    retdata = deepcopy(data)

    # Pre filter.
    prefilter = norm * fraction / data.size

    # Transform to dictionary
    dlist = {}
    snorm = spacing[0] * spacing[1] * spacing[2]
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                val = data[i, j, k] * snorm
                if val > prefilter:
                    dlist[(i, j, k)] = val
                else:
                    retdata[i, j, k] = 0

    # Binary search filter.
    keylist = list(sorted(dlist, key=dlist.get))
    left = 0
    right = len(keylist)
    while (True):
        if left == right or left == right - 1:
            break
        mid = int((right - left)/2) + left
        sumval = sum([dlist[k] for k in keylist[:mid]])
        if sumval < norm - norm*fraction:
            left = mid
        else:
            right = mid

    # Filter data
    for k in keylist[right:]:
        retdata[k[0], k[1], k[2]] = 0

    return retdata


def apply_polynomial(data, polynomial):
    """
    Raise each value in an array to a given exponent.

    Args:
        data (list): 3d data array.
        polynomial(str): the polynomial to apply to.
    """
    from sympy.parsing.sympy_parser import parse_expr
    from sympy.utilities.lambdify import lambdify
    from sympy.abc import x

    expr = parse_expr(polynomial)
    fun = lambdify(x, expr)
    return fun(data)


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


def compute_volume(data, spacing):
    """
    Compute the volume of the isosurface.

    Args:
        data (list): the 3d underlying data.
        spacing (list): the grid spacing.

    Returns:
        (float): the volume.
    """
    volume = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                volume += data[i, j, k]*spacing[0]*spacing[1]*spacing[2]

    return volume


def visualize(verts, faces, grid_points, spacing):
    """
    Visualize an isosurface.

    Args:
        verts (list): list of vertices.
        faces (list): list of points defining the triangles.
        grid_points (list): the data.
        spacing (list): the grid spacing.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    triangles = []
    for f in faces:
        tri = (verts[f[0]], verts[f[1]], verts[f[2]])
        triangles.append(tri)

    axs = plt.subplot(projection="3d")

    col = Poly3DCollection(triangles, color="blue")
    axs.add_collection(col)

    axs.set_xlim([0, grid_points[0]*spacing[0]])
    axs.set_ylim([0, grid_points[1]*spacing[1]])
    axs.set_zlim([0, grid_points[2]*spacing[2]])

    plt.show()
