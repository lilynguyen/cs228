__author__ = 'Lily H. Nguyen'
__date__ = '11/13/15'

# -----------------------------------------
# FINAL PROJECT - CS 228 HUMAN COMPUTER INTERACTION
# Learning American Sign Language with Leap Motion
# Version Goals: modularize, classify
#
# application.py looks like utter shit lol
# -----------------------------------------

import sys
import thread
import time
import random
import timeit

import matplotlib
import Leap
import pickle
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D

# -----------------------------------------
# 								CLASS GUI
# -----------------------------------------

class GUI():
	def __init__(self):
		self.gestureImages = ['./images/gesture0.png',
			'./images/gesture1.png',
			'./images/gesture2.png',
			'./images/gesture3.png',
			'./images/gesture4.png',
			'./images/gesture5.png',
			'./images/gesture6.png',
			'./images/gesture7.png',
			'./images/gesture8.png',
			'./images/gesture9.png']

		self.digitImages = ['./images/digit0.png',
			'./images/digit1.png',
			'./images/digit2.png',
			'./images/digit3.png',
			'./images/digit4.png',
			'./images/digit5.png',
			'./images/digit6.png',
			'./images/digit7.png',
			'./images/digit8.png', 
			'./images/digit9.png']

		self.positionImages = ['./images/centered.png',
			'./images/left.png',
			'./images/right.png',
			'./images/over.png']

		self.statusImages = ['./images/check.png',
			'./iamges/x.png']

		matplotlib.interactive(True)
		gs = gridspec.GridSpec(3,2) # Layout manager
		fig = plt.figure(figsize=(8,6), facecolor="black") # Actual window

		self.handPanel = fig.add_subplot(gs[:,0], projection='3d')
		self.handPanel.set_xlim(-200, 200)
		self.handPanel.set_ylim(0, 300)
		self.handPanel.set_zlim(0, 300)
		self.handPanel.view_init(azim=90)
		self.handPanel.axis("off")

		self.positionPanel = fig.add_subplot(gs[0,1])
		self.positionPanel.axis('off')

		self.gesturePanel = fig.add_subplot(gs[1,1])
		self.gesturePanel.axis('off')

		self.countPanel = fig.add_subplot(gs[2,1])
		self.countPanel.axis('off')

		plt.draw()

	def updateHandPanel(self, lines, xBase, xTip, zBase, zTip, yBase, yTip):
		lines.append(self.handPanel.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))

	def updatePositionPanel(self, side):
		self.clearPositionPanel()
		imageLocation = self.positionImages[side]
		image = mpimg.imread(imageLocation)
		self.positionPanel.imshow(image)

	def updateGesturePanel(self, gestureNum, phase):
		self.clearGesturePanel()

		if phase == SHOW_GESTURE:
			imageLocation = self.gestureImages[gestureNum]
			image = mpimg.imread(imageLocation)
			self.gesturePanel.imshow(image)

		elif phase == CORRECT_INCORRECT:
			if gestureNum == CORRECT:
				imageLocation = self.statusImages[gestureNum]

			elif gestureNum == INCORRECT:
				imageLocation = self.statusImages[gestureNum]

			image = mpimg.imread(imageLocation)
			self.gesturePanel.imshow(image)
			time.sleep(1)

	def updateCountPanel(self, gestureNum, phase, database, userName):
		userRecord = database[userName]

		self.clearCountPanel()
		digitString = 'digit' + str(gestureNum) + 'attempts'

		if phase == DISPLAY_NUM:
			displayCount = str(userRecord[digitString])
		elif phase == UPDATE_NUM:
			displayCount = str(userRecord[digitString]) + '+ 1'

		self.countPanel.text(0.5,0.5, displayCount, color='white', fontsize=15)

	def clearHandPanel(self, lines):
		plt.draw()
		while (len(lines) > 0):
			ln = lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []

	def clearPositionPanel(self):
		self.positionPanel.clear()
		self.positionPanel.axis('off')

	def clearGesturePanel(self):
		self.gesturePanel.clear()
		self.gesturePanel.axis('off')

	def clearCountPanel(self):
		self.countPanel.clear()
		self.countPanel.axis('off')

# -----------------------------------------
# 								CONSTANTS
# -----------------------------------------

CENTER = 0
LEFT = 1
RIGHT = 2
MISSING = 3

DISPLAY_NUM = 0
UPDATE_NUM = 1

CORRECT = 0
INCORRECT = 1

CENTER_RANGE = 100

SHOW_GESTURE = 0
CORRECT_INCORRECT = 1

# -----------------------------------------
# 				BEGIN MAIN GAME PROCESS
# -----------------------------------------

def main():
	database = pickle.load(open('userData/database.p','rb'))
	clf = pickle.load(open('userData/classifier.p','rb'))

	controller = Leap.Controller()
	testData = np.zeros((1,30),dtype='f')

	userName = get_username()
	userExists = user_database_checker(userName, database)
	userNameFormatted = get_formatted_username(userName)

	if userExists:
		print('Welcome back ' + userNameFormatted + '!')
	else:
		print('Welcome ' + userNameFormatted + '!')

	gestureNum = 0 # Start at 0 for game.
	add_attempt(userName, gestureNum, database)

	#startTime = timeit.default_timer()

	print database

	gui = GUI()
	gui.updateGesturePanel(gestureNum, SHOW_GESTURE)
	gui.updateCountPanel(gestureNum, DISPLAY_NUM, database, userName)

	# -----------------------------------------
	# 					BEGIN MAIN GAME LOOP
	# -----------------------------------------
	while True:
		frame = controller.frame()
		lines = []
		k = 0
		hand = frame.hands[0]

		for i in range(0,5):
			finger = hand.fingers[i]

			for j in range (0,4):
				bone = finger.bone(j)
				boneBase = bone.prev_joint
				boneTip = bone.next_joint

				xTip = boneTip[0]
				yTip = boneTip[1]
				zTip = boneTip[2]
				xBase = boneBase[0]
				yBase = boneBase[1]
				zBase = boneBase[2]

				gui.updateHandPanel(lines, xBase, xTip, zBase, zTip, yBase, yTip)

				if ((j == 0) | (j == 3)):
					testData[0,k] = xTip
					testData[0,k+1] = yTip
					testData[0,k+2] = zTip
					k = k + 3

		gui.clearHandPanel(lines)

		#-----------------------------------------
		# STATE: HAND NOT IN FRAME
		#-----------------------------------------
		if len(frame.hands) == 0:
			gui.updatePositionPanel(MISSING)
			print "No Hand"

		#-----------------------------------------
		# STATE: HAND IN FRAME
		#-----------------------------------------
		elif len(frame.hands) == 1:
			print "Hand"

			#-----------------------------------------
			# STATE: HAND IN FRAME TOO LEFT
			#-----------------------------------------
			if min(testData[0, 0::3]) < -CENTER_RANGE:
				gui.updatePositionPanel(LEFT)

			#-----------------------------------------
			# STATE: HAND IN FRAME TOO RIGHT
			#-----------------------------------------
			elif max(testData[0, 0::3]) > CENTER_RANGE:
				gui.updatePositionPanel(RIGHT)

			#-----------------------------------------
			# STATE: HAND IN FRAME CENTER
			#-----------------------------------------
			elif (min(testData[0, ::3]) > -CENTER_RANGE) and (max(testData[0, ::3]) < CENTER_RANGE):
				gui.updatePositionPanel(CENTER)

				predictedGesture = predict_data(testData, clf)

				if int(predictedGesture) == gestureNum:
					gui.updateCountPanel(gestureNum, UPDATE_NUM, database, userName)
					gui.updateGesturePanel(CHECK, CORRECT_INCORRECT)

					gestureNum += 1

					add_attempt(userName, gestureNum, database)
					gui.updateCountPanel(gestureNum, DISPLAY_NUM, database, userName)
					gui.updateGesturePanel(gestureNum, SHOW_GESTURE)


# -----------------------------------------
# 								FUNCTIONS
# -----------------------------------------

def get_username():
	userName = raw_input('Enter Name: ')
	userNameLower = userName.lower()
	return userNameLower

def get_formatted_username(userName):
	userNameFormatted = userName[0].upper() + userName[1:]
	return userNameFormatted

def user_database_checker(userName, database):

	if userName in database:
		userRecord = database[userName]
		userRecord['logins'] += 1
		return True

	elif userName not in database:
		database[userName] = {}
		userRecord = database[userName]
		userRecord['logins'] = 1
		return False

	pickle.dump(database, open('userData/database.p','wb'))

def add_attempt(userName, gestureNum, database):
	digitString = 'digit'+str(gestureNum)+'attempts'
	userRecord = database[userName]

	print 'Adding 1 to', digitString

	if digitString in userRecord:
		print digitString, 'exists in database for', userName
		userRecord[digitString] += 1

	elif digitString not in userRecord:
		print 'Adding', digitString, 'to database for', userName
		userRecord[digitString] = 1

	pickle.dump(database, open('userData/database.p','wb'))

def center_data(testData):
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

def predict_data(testData, clf):
	centeredData = center_data(testData)
	predictedGesture = clf.predict(centeredData)
	return predictedGesture

main()