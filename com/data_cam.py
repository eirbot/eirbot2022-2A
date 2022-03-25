import numpy as np

def EnvoiCoord():
    A = np.zeros(2, dtype=int)
    A[0] = np.trunc(np.random.rand(1)*512)
    A[1] = np.trunc(np.random.rand(1)*512)
    coord_pos = [int(A[0]), int(A[1])]
    return coord_pos


coord = EnvoiCoord()
coord2 = str(coord);
coord3 = coord2[1:len(coord2)-1]
coord4 = coord3.replace(" ","")
print(coord4)
