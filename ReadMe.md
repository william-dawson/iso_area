# Iso Area 

This script takes in a gaussian cube file and an iso-level value, and produces:
1) the surface area of the isosurface
2) the volume of the isosurface shape. 

For the definition of volume, data values are masked to 1 or 0 based
on the isosurface value. Thus this is just a rough measure of the size of the
isosurface, since a wavefunction is a normalized quantity. Example usage:
```
python compute.py test.cube 0.5
```
This script requires you to install `scikit-image`, which can be done with
pip or conda.

As a sanity check you can also visualize the isosurface:
```
python compute.py test.cube 0.5 --visualize True
```
