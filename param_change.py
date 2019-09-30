import os
import numpy as np

par_files = os.listdir('parameters/')

for p in par_files:
    print('processing ' + p)
    with open('parameters/'+p, 'r') as f:
        read_file = f.read()

    read_file = np.array(read_file.split('\n'), dtype = '<U80')

    read_file[43] = 'delta_ra = 0.5/60 #degrees'
    read_file[44] = 'delta_dec = 0.5/60 #degrees'

    with open('parameters/'+p,'w') as f:
        for i in read_file:
            f.write(i+'\n')
