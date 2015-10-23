import numpy as np
import pickle
from sklearn import neighbors, datasets

fileName = 'userData/Margolis_train0.p'
f = open(fileName,'rb')
train0 = pickle.load(f)

fileName = 'userData/Margolis_test0.p'
f = open(fileName,'rb')
test0 = pickle.load(f)

fileName = 'userData/train1.p'
f = open(fileName,'rb')
train1 = pickle.load(f)

fileName = 'userData/test1.p'
f = open(fileName,'rb')
test1 = pickle.load(f)

fileName = 'userData/Sheehan_train2.p'
f = open(fileName,'rb')
train2 = pickle.load(f)

fileName = 'userData/Sheehan_test2.p'
f = open(fileName,'rb')
test2 = pickle.load(f)

fileName = 'userData/Siegel_train3.p'
f = open(fileName,'rb')
train3 = pickle.load(f)

fileName = 'userData/Siegel_test3.p'
f = open(fileName,'rb')
test3 = pickle.load(f)

fileName = 'userData/train4.p'
f = open(fileName,'rb')
train4 = pickle.load(f)

fileName = 'userData/test4.p'
f = open(fileName,'rb')
test4 = pickle.load(f)

fileName = 'userData/Siegel_train5.p'
f = open(fileName,'rb')
train5 = pickle.load(f)

fileName = 'userData/Siegel_test5.p'
f = open(fileName,'rb')
test5 = pickle.load(f)

fileName = 'userData/train6.p'
f = open(fileName,'rb')
train6 = pickle.load(f)

fileName = 'userData/test6.p'
f = open(fileName,'rb')
test6 = pickle.load(f)

fileName = 'userData/White_train7.p'
f = open(fileName,'rb')
train7 = pickle.load(f)

fileName = 'userData/White_test7.p'
f = open(fileName,'rb')
test7 = pickle.load(f)

fileName = 'userData/train8.p'
f = open(fileName,'rb')
train8 = pickle.load(f)

fileName = 'userData/test8.p'
f = open(fileName,'rb')
test8 = pickle.load(f)

fileName = 'userData/train9.p'
f = open(fileName,'rb')
train9 = pickle.load(f)

fileName = 'userData/test9.p'
f = open(fileName,'rb')
test9 = pickle.load(f)


def ReshapeData(set0, set1, set2, set3, set4, set5, set6, set7, set8, set9):
	X = np.zeros((10000,5*2*3),dtype='f') # 1000 * 2 training points, 5*4*6 (120) features
	y = np.zeros((10000)) # 1000 * 2 training points, just one feature...one dimensional or what

	for i in range(0,1000):
		n = 0
		for j in range(0,5):
			for k in range(0,2): # 2 bones, naw 4
 				for m in range(0,3): # tips aka squares 3-6 see diagram WHY ISNT THIS 3-6
					X[i, n] = set0[j,k,m,i]
					X[i+1000, n] = set1[j,k,m,i]
					X[i+2000, n] = set2[j,k,m,i]
					X[i+3000, n] = set3[j,k,m,i]
					X[i+4000, n] = set4[j,k,m,i]
					X[i+5000, n] = set5[j,k,m,i]
					X[i+6000, n] = set6[j,k,m,i]
					X[i+7000, n] = set7[j,k,m,i]
					X[i+8000, n] = set8[j,k,m,i]
					X[i+9000, n] = set9[j,k,m,i]

					y[i] = "0" # first 1000 points belong to class zero ### CHANGED
					y[i+1000] = "1" # second 1000 points belong to class one ### CHANGED
					y[i+2000] = "2"
					y[i+3000] = "3"
					y[i+4000] = "4"
					y[i+5000] = "5"
					y[i+6000] = "6"
					y[i+7000] = "7"
					y[i+8000] = "8"
					y[i+9000] = "9"
					n = n + 1
	return X, y

def ReduceData(X):
	X = np.delete(X,1,1) # cut out proximal phalange
	X = np.delete(X,1,1) # cut out intermediate phalange
	X = np.delete(X,0,2)
	X = np.delete(X,0,2)
	X = np.delete(X,0,2)

	return X

def CenterData(X):

	# center x coordinates
	allXCoordinates = X[:,:,0,:]
	meanValue = allXCoordinates.mean()
	X[:,:,0,:] = allXCoordinates - meanValue

	# center y coordinates
	allYCoordinates = X[:,:,1,:]
	meanValue = allYCoordinates.mean()
	X[:,:,1,:] = allYCoordinates - meanValue

	# center z coordinates
	allZCoordinates = X[:,:,2,:]
	meanValue = allZCoordinates.mean()
	X[:,:,2,:] = allZCoordinates - meanValue

	return X


train0 = ReduceData(train0)
test0 = ReduceData(test0)
train1 = ReduceData(train1)
test1 = ReduceData(test1)
train2 = ReduceData(train2)
test2 = ReduceData(test2)
train3 = ReduceData(train3)
test3 = ReduceData(test3)
train4 = ReduceData(train4)
test4 = ReduceData(test4)
train5 = ReduceData(train5)
test5 = ReduceData(test5)
train6 = ReduceData(train6)
test6 = ReduceData(test6)
train7 = ReduceData(train7)
test7 = ReduceData(test7)
train8 = ReduceData(train8)
test8 = ReduceData(test8)
train9 = ReduceData(train9)
test9 = ReduceData(test9)

train0 = CenterData(train0)
test0 = CenterData(test0)
train1 = CenterData(train1)
test1 = CenterData(test1)
train2 = CenterData(train2)
test2 = CenterData(test2)
train3 = CenterData(train3)
test3 = CenterData(test3)
train4 = CenterData(train4)
test4 = CenterData(test4)
train5 = CenterData(train5)
test5 = CenterData(test5)
train6 = CenterData(train6)
test6 = CenterData(test6)
train7 = CenterData(train7)
test7 = CenterData(test7)
train8 = CenterData(train8)
test8 = CenterData(test8)
train9 = CenterData(train9)
test9 = CenterData(test9)

trainX, trainy = ReshapeData(train0, train1, train2, train3, train4, train5, train6, train7, train8, train9)
testX, testy = ReshapeData(test0, test1, test2, test3, test4, test5, test6, test7, test8, test9)

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX,trainy)

counter = 0
for i in range(10000):
	if clf.predict(testX[i,:]) == int(testy[i]):
		counter += 1
print float(counter/10000)*100, '%'

pickle.dump(clf, open('userData/classifier.p','wb'))