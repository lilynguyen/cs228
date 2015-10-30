import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import pickle
import numpy as np

def main():
	controller = Leap.Controller()
	CreateGraph()

	# read in classifier
	clf = pickle.load(open('userData/classifier.p','rb'))

	# create 1x30 array, [x1,y1,z1,x2,y2,z2...etc] only the metacarpal, distal tips
	testData = np.zeros((1,30),dtype='f')

def CreateGraph():
	matplotlib.interactive(True)
	fig = plt.figure(figsize=(8,6))
	ax = fig.add_subplot(111,projection='3d')
	ax.set_xlim(-328.471557617,306.569793701)
	ax.set_ylim(43.1206054688,606.693664551)
	ax.set_zlim(-30.4142894745,511.524658203)
	ax.view_init(azim=90)
	plt.draw()

def CenterData(testData):
	allXCoordinates = testData[0,::3]
	meanValue = allXCoordinates.mean()
	testData[0,::3] = allXCoordinates - meanValue

	allYCoordinates = testData[0,1::3]
	meanValue = allYCoordinates.mean()
	testData[0,1::3] = allYCoordinates - meanValue

	allZCoordinates = testData[0,2::3]
	meanValue = allZCoordinates.mean()
	testData[0,2::3] = allZCoordinates - meanValue

	return testData

while (True):
	frame = controller.frame()
	lines = []
	hands = frame.hands

	if len(hands): # If hands = 1, aka bool TRUE
		k = 0

		# want single hand
		hand = frame.hands[0]

		# iterate over each of the five fingers
		for i in range(0,5):

			# list of fingers in hand
			fingerList = hand.fingers

			# getting actual finger
			finger = fingerList[i]

			# iterate through the four major bones
			for j in range(0,4):
				bone = finger.bone(j)
				boneBase = bone.prev_joint
				boneTip = bone.next_joint

				xTip = boneTip[0]
				yTip = boneTip[1]
				zTip = boneTip[2]
				xBase = boneBase[0]
				yBase = boneBase[1]
				zBase = boneBase[2]

				lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))

				if ((j == 0) | (j == 3)):
					testData[0,k] = xTip
					testData[0,k+1] = yTip
					testData[0,k+2] = zTip
					k = k + 3

		print testData

		testData = CenterData(testData)
		predictedClass = clf.predict(testData)
		print predictedClass

		plt.draw()

		while (len(lines) > 0):
			ln = lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []
