import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

TYPE_INDEX = 1
TYPE_DISTAL = 3

class Deliverable:
	def __init__(self):

		self.numberOfGesturesSaved = 0
		self.previousNumberOfHands = 0
		self.currentNumberOfHands = 0

		self.gestureData = np.zeros((5,4,6),dtype='f')
		self.controller = Leap.Controller()
		self.lines = []
		matplotlib.interactive(True)
		fig = plt.figure(figsize=(8,6))
		self.ax = fig.add_subplot(111,projection='3d')

		self.ax.set_xlim(-328.471557617,306.569793701)
		self.ax.set_ylim(43.1206054688,606.693664551)
		self.ax.set_zlim(-30.4142894745,511.524658203)

		plt.draw()

	def HandleBone(self,i,j):
		#print "RUNNING HANDLEBONE"

		# iterate through the four major bones
		bone = self.finger.bone(j)
		boneBase = bone.prev_joint
		boneTip = bone.next_joint

		xTip = boneTip[0]
		yTip = boneTip[1]
		zTip = boneTip[2]
		xBase = boneBase[0]
		yBase = boneBase[1]
		zBase = boneBase[2]

		#print self.numberOfHands

		if (self.currentNumberOfHands == 1):
			self.lines.append(self.ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'g'))
		# else:
		# 	self.lines.append(self.ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))
		elif (self.currentNumberOfHands == 2):
			self.lines.append(self.ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))

		# if the second hand is taken out of the frame, record the gesutres into gestureData
		if (self.RecordingIsEnding()):
			# bone j finger i
			self.gestureData[i,j,0] = xBase
			self.gestureData[i,j,1] = yBase
			self.gestureData[i,j,2] = zBase
			self.gestureData[i,j,3] = xTip
			self.gestureData[i,j,4] = yTip
			self.gestureData[i,j,5] = zTip

	def HandleFinger(self,i):
		#print "RUNNING HANDLEFINGER"

		# list of fingers in hand
		fingerList = self.hand.fingers

		# get each finger as loop iterates
		self.finger = fingerList[i]

		# call handlebone on each of the finger
		for j in range(0,4):

			# CALL HANDLEBONE
			self.HandleBone(i,j)

	def RecordingIsEnding(self):
		return (self.previousNumberOfHands == 2) & (self.currentNumberOfHands == 1)

	def SaveGesture(self):

		self.numberOfGesturesSaved += 1

		print ("Saved Gesture " + str(self.numberOfGesturesSaved))

		# k is the number of the file
		# this saves the gestures to their own files
		fileName = 'userData/gesture'+str(self.numberOfGesturesSaved-1)+'.dat'
		f = open(fileName,'w')
		np.save(f,self.gestureData) # saves matrix self.gestureData to the file
		f.close()

		# this is the number of gestures recorded
		fileName = 'userData/numOfGestures.dat'
		f = open(fileName,'w')
		f.write(str(self.numberOfGesturesSaved))
		f.close()

	def HandleHands(self):
		#print "RUNNING HANDLEHANDS"
		#print len(self.frame.hands)

		self.previousNumberOfHands = self.currentNumberOfHands

		# finds number of hands in frame
		self.currentNumberOfHands = len(self.frame.hands)

		# want single hand
		self.hand = self.frame.hands[0]

		for i in range(0,5):

				#CALL HANDLEFINGER
				self.HandleFinger(i)

		plt.draw()

		# Erases the lines so hand movements don't track
		while (len(self.lines) > 0):
			ln = self.lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []

		# Prints every time red hand is taken awy
		if (self.RecordingIsEnding()):
			#print 'Recording is Ending'

			# right now this is giving you the coordinates for the top of the thumb distal
			print self.gestureData[:,:,:]

			# CALL SAVEGESTURE
			self.SaveGesture()

	def RunOnce(self):
		#print "RUNNING RUNONCE"

		self.frame = self.controller.frame()
		self.hands = self.frame.hands # this line is redundy but like just keep it
		
		# If hands = 1, aka bool TRUE
		if len(self.hands):

			# CALL HANDLEHANDS
			self.HandleHands()

			self.ax.view_init(azim=90)

	def RunForever(self):
		#print "RUNNING RUNFOREVER"

		while (True):
			self.RunOnce()

deliverable = Deliverable()
deliverable.RunForever()