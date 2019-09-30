import os
import pandas as pd

files = os.listdir('catalogues')

names = [x.split('.')[0] for x in files]

status = ['pending']*len(names)

d = {'Name':sorted(names), 'Status':status}
d = pd.DataFrame(data=d)
d.to_csv('mf_log.txt', index=False, sep = '\t')
