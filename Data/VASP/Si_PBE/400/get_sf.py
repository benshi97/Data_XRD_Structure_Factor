

import numpy as np
import matplotlib.pyplot as plt

def get_sf_vasp(core_ae,val_scf):
    with open(core_ae,'r') as myfile:
        fftgrid = np.array([0,0,0])
        latticevectors = np.zeros((3,3))
        dummyboolean = False
        for i, line in enumerate(myfile):
            if i == 2:
                latticevectors[0] = np.array(line.split()).astype(np.float)
            elif i == 3:
                latticevectors[1] = np.array(line.split()).astype(np.float)
            elif i == 4:
                latticevectors[2] = np.array(line.split()).astype(np.float)
            elif line.isspace():
                dummy_index = i+2
                dummyboolean = True
            elif dummyboolean == True:
                fftgrid = np.array(line.split()).astype(np.int)
                break
    den = np.loadtxt(core_ae,skiprows = dummy_index)+ \
          np.loadtxt(val_scf,skiprows = dummy_index)
    den = den.ravel()
    den = den.reshape(fftgrid,order='F')
    # grid_point_volume = np.linalg.det(latticevectors)/np.prod(fftgrid)
    sf=np.fft.ifftn(den)
    return sf[0:10,0:10,0:10]

a = get_sf_vasp('AECCAR0','AECCAR2')

np.save('structurefactors.npy',a)

print(abs(a[0,0,0]),abs(a[1,1,1]))
