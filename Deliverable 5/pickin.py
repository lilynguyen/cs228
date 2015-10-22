import pickle
import numpy as np

fileName = 'userData/train7.dat'
INFO = np.load(open(fileName,'r'))
pickle.dump(INFO,open(fileName,'w'))


fileName = 'userData/train8.dat'
INFO = np.load(open(fileName,'r'))
pickle.dump(INFO,open(fileName,'w'))


fileName = 'userData/test7.dat'
INFO = np.load(open(fileName,'r'))
pickle.dump(INFO,open(fileName,'w'))


fileName = 'userData/test8.dat'
INFO = np.load(open(fileName,'r'))
pickle.dump(INFO,open(fileName,'w'))
