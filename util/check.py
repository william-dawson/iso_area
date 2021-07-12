"""
Generates 1/8 of a sphere to check against.
"""
from numpy import zeros
from numpy.linalg import norm

size = 40
spacing = 1.0/size
data = zeros((size, size, size))

for i in range(size):
    for j in range(size):
        for k in range(size):
            dist = norm([i*spacing, j*spacing, k*spacing])
            if dist < 1.0:
                data[i, j, k] = 1.0

with open("test.cube", "w") as ofile:
    ofile.write("Test cube file\n")
    ofile.write("\n")
    ofile.write("0 0 0 0 1\n")
    ofile.write(str(size) + " " + str(spacing) + " 0 0\n")
    ofile.write(str(size) + " 0 " + str(spacing) + " 0\n")
    ofile.write(str(size) + " 0 0 " + str(spacing) + "\n")
    ofile.write("1 1\n")

    c = 0
    for i in range(size):
        for j in range(size):
            for k in range(size):
                ofile.write(str(data[i, j, k]))
                c += 1
                if c == 6:
                    ofile.write("\n")
                    c = 0
                else:
                    ofile.write(" ")
