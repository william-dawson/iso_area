# Iso Area 

This script requires you to install `scikit-image` and `sympy`, which can be
done with pip or conda.

The usage of the code is:
```
python power.py test.cube 1.0 0.01 "x**(5/3)" --visualize False
```

The first argument is the cube file to analyze. This data is read in, and the
density is computed by squaring each value. 

The second argument is the normalization. Since the grid is usually too
coarse, we manually renormalize so that the sum of the density is one.

The third argument is the fraction of the density we want to consider. For
example, `0.01` means 99%. An isosurface of the density is computed such that
that percentage of the data is contained within it.

The fourt argument is a function to apply to the data. `x` should be the name
of the dependent variable.

Finally, the constructed isosurface can be visualized as an optional parameter,
using values `True` or `False`.

After the calculation is run, three values are printed. First is the `Filtered
Volume` which is the amount of volume removed by the filtering process. This
should be very close to the value you input as the second parameter.

Next is the `Sum` which is the sum of the function on all points inside 
the isosurface. The average is that value divided by the size of the whole
domain and divided by the volume contained with the isosurface.
