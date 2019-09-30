from parameters.tuc2_pars import pos
name = 'tuc2.dat'

import pandas as pd

d = pd.read_table('catalogues/'+name, delimiter = '\s+', header=None)
d = d.iloc[:,:9]

cond1 = (d.iloc[:,1] <= pos[0] + 0.5) & (d.iloc[:,1] >= pos[0] - 0.5)
cond2 = (d.iloc[:,2] <= pos[1] + 0.5) & (d.iloc[:,2] >= pos[1] - 0.5)

d = d.loc[cond1 & cond2, :]
d.to_csv('catalogues/'+name, sep = ' ', header=None, index=False)
