import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import pickle
import numpy as np

controller = Leap.Controller()

matplotlib.interactive(True)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111,projection='3d')
plt.draw()

clf = pickle.load(open('userData/classifier.p','rb'))
testData = np.zeros((1,30),dtype='f')

def CenterData(testData):

	#print "FIRST", testData

	arrayX = testData[0,::3]
	meanX = arrayX.mean()
	testData[0,::3] =- meanX

	print "way 1", testData

	testData[0,::3] =- testData[0,::3].mean()

	print "way 2", testData

	testData[0,1::3] =- testData[0,1::3].mean()
	testData[0,2::3] =- testData[0,2::3].mean()

	#print "SECOND", testData

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
					k += 3

			CenterData(testData)

		testData = CenterData(testData)
		predictedClass = clf.predict(testData)
		print predictedClass

		ax.set_xlim(-328.471557617,306.569793701)
		ax.set_ylim(43.1206054688,606.693664551)
		ax.set_zlim(-30.4142894745,511.524658203)

		ax.view_init(azim=90)

		plt.draw()

		while (len(lines) > 0):
			ln = lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []
