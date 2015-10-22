import numpy as np
import pickle
from sklearn import neighbors, datasets

fileName = 'userData/train7.p'
f = open(fileName,'r')
train7 = pickle.load(f)
f.close()

fileName = 'userData/train8.p'
f = open(fileName,'r')
train8 = pickle.load(f)
f.close()

fileName = 'userData/test7.p'
f = open(fileName,'r')
test7 = pickle.load(f)
f.close()

fileName = 'userData/test8.p'
f = open(fileName,'r')
test8 = pickle.load(f)
f.close()

def ReshapeData(set1,set2):
	X = np.zeros((2000,5*2*3),dtype='f') # 1000 * 2 training points, 5*4*6 (120) features
	y = np.zeros((2000),dtype='f') # 1000 * 2 training points, just one feature...one dimensional or what

	# i is number of gestures recorded
	# j is number of fingers
	# k is number of bones
	# m is tip coordinates

	for i in range(0,1000):
		n = 0
		for j in range(0,5):
			for k in range(0,2): # 2 bones, naw 4
 				for m in range(0,3): # tips aka squares 3-6 see diagram WHY ISNT THIS 3-6
					X[i,n] = set1[j,k,m,i]
					X[i+1000,n] = set2[j,k,m,i]
					y[i] = 7 # first 1000 points belong to class zero ### CHANGED
					y[i+1000] = 8 # second 1000 points belong to class one ### CHANGED
					n += 1
	return X, y

def ReduceData(X):
	X = np.delete(X,1,1) # cut out proximal phalange
	X = np.delete(X,1,1) # cut out intermediate phalange

	X = np.delete(X,0,2)

	return X

def CenterData(X):

	# center x coordinates
	allXCoordinates = X[:,:,0,:]
	meanValue = allXCoordinates.mean()
	X[:,:,0,:] = allXCoordinates - meanValue

	# center y coordinates
	allYCoordinates = X[:,0,:,:]
	meanValue = allYCoordinates.mean()
	X[:,0,:,:] = allYCoordinates - meanValue

	# center z coordinates
	allZCoordinates = X[0,:,:,:]
	meanValue = allZCoordinates.mean()
	X[0,:,:,:] = allZCoordinates - meanValue

	return X

train7 = ReduceData(train7)
train8 = ReduceData(train8)
test7 = ReduceData(test7)
test8 = ReduceData(test8)

train7 = CenterData(train7)
train8 = CenterData(train8)
test7 = CenterData(test7)
test8 = CenterData(test8)

trainX, trainy = ReshapeData(train7,train8)
testX, testy = ReshapeData(test7,test8)

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX,trainy)

pickle.dump(clf, open('userData/classifier.p','wb'))