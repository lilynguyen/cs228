import pickle
import numpy as np

fileName = 'userData/train7.p'
f = open(fileName,'r')
DATA = pickle.load(f)
pickle.dump(DATA, open(fileName,'wb'))


fileName = 'userData/train8.p'
f = open(fileName,'r')
DATA = pickle.load(f)
pickle.dump(DATA, open(fileName,'wb'))


fileName = 'userData/test7.p'
f = open(fileName,'r')
DATA = pickle.load(f)
pickle.dump(DATA, open(fileName,'wb'))


fileName = 'userData/test8.p'
f = open(fileName,'r')
DATA = pickle.load(f)
pickle.dump(DATA, open(fileName,'wb'))
