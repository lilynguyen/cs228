import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors, datasets

# the iris data set (150 flowers, 4 features)
# sepal length, sepal width, petal length, petal width
iris = datasets.load_iris()

# # 0 to 149 items, all 4 columns
# for i in range(len(iris.data)):
# 	print i, iris.data[i]

# # 0 to 149 items, just sepal length & sepal width
# for i in range(len(iris.data)):
# 	print i, iris.data[i,0:2]

# species ID, only 3 species
# print iris.target

trainX = iris.data[::2,0:2]
trainy = iris.target[::2]

testX = iris.data[1::2,0:2]
testy = iris.target[1::2]

colors = np.zeros((3,3),dtype='f')
colors[0,:] = [1,0.5,0.5] # red
colors[1,:] = [0.5,1,0.5] # green
colors[2,:] = [0.5,0.5,1] # blue

clf = neighbors.KNeighborsClassifier(15)
clf.fit(trainX,trainy)

# itemIndex = 50
# actualClass = testy[itemIndex]
# prediction = clf.predict(testX[itemIndex,0:2])
# print actualClass, prediction

plt.figure()

########## ODD ##########

# x = trainX[:,0]
# y = trainX[:,1]
# plt.scatter(x,y,c=trainy)

########## EVEN ##########

# x = testX[:,0]
# y = testX[:,1]
# plt.scatter(x,y,c=testy)


[numItems,numFeatures] = iris.data.shape

### ACTUAL ###
for i in range(0,numItems/2):
	itemClass = int(trainy[i])
	currColor = colors[itemClass,:]
	plt.scatter(trainX[i,0],trainX[i,1],facecolor=currColor,s=50,lw=2)

### PREDICT ###
predictionsRight = 0
for i in range(0,numItems/2):
	prediction = int(clf.predict(testX[i,:]))
	edgeColor = colors[prediction,:]

	if prediction == int(testy[i]):
		predictionsRight += 1

	itemClass = int(trainy[i]) # KEEP THIS THE SAME
	currColor = colors[itemClass,:] # KEEP THIS THE SAME
 	plt.scatter(testX[i,0],testX[i,1],facecolor=currColor,s=50,lw=2,edgecolor=edgeColor)
print predictionsRight

plt.show()