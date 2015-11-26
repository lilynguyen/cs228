import sys
import os
import thread
import threading
import time

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from mpl_toolkits.mplot3d import Axes3D

from threading import Timer

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec

# =========================================
# 								GUI CLASS
# =========================================

class GUI():
	def __init__(self):

		# --------- IMAGE LISTS ---------
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

		self.programImages = ['./images/logo.png',
			'./images/begin.png',
			'./images/hover.png']

		# ------ GLOBAL VARIABLES ------
		self.lines = []
		self.dis_already = False

		# ------ WINDOW SETTINGS  ------
		mpl.interactive(True)
		mpl.rcParams['toolbar'] = 'None'
		self.fig = plt.figure(figsize=(15,10), facecolor='black')
		#self.fig.canvas.set_window_title('signum')

		# ------ PANEL INITS -----------
		self.splashPanel = ''
		self.beginPanelTitle = ''
		self.beginPanelImg = ''
		self.handPanel = ''

	def setup_splashPanel(self):
		self.splashPanel = self.fig.add_subplot(111)
		self.splashPanel.axis('off')

	def setup_beginPanel(self):
		gs = gridspec.GridSpec(5,1)

		self.beginPanelTitle = self.fig.add_subplot(gs[0,0])
		self.beginPanelTitle.axis('off')

		self.beginPanelImg = self.fig.add_subplot(gs[1:4,0])
		self.beginPanelImg.axis('off')

	def setup_handPanel(self):
		self.handPanel = self.fig.add_subplot(111, projection='3d', axisbg='none', frame_on=False)
		self.handPanel.view_init(azim=90)
		self.handPanel.set_xlim(-50,50)
		self.handPanel.set_ylim(150,200)
		self.handPanel.set_zlim(400,550)
		self.handPanel.axis('off')
#-----------------------------------------------
	def draw_hand(self, frame):
		hands = frame.hands

		if len(hands):
			hand = frame.hands[0]

			for i in range(0,5):
				finger = hand.fingers[i]

				for j in range(0,3):
					bone = finger.bone(j)

					boneBase = bone.prev_joint
					boneTip = bone.next_joint

					xTip = boneTip[0]
					yTip = boneTip[1]
					zTip = boneTip[2]
					xBase = boneBase[0]
					yBase = boneBase[1]
					zBase = boneBase[2]

					self.lines.append(self.handPanel.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip], \
						color='red', linewidth=25, solid_capstyle='round'))

			plt.draw()
			self.clear_hand_tracing()

	def clear_hand_tracing(self):
		while (len(self.lines) > 0):
			ln = self.lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []
#-----------------------------------------------
	def splash_screen(self):
		imageLocation = self.programImages[0]
		image = mpimg.imread(imageLocation)
		self.splashPanel.imshow(image)
		plt.draw()

		time.sleep(2)

		self.fig.delaxes(self.splashPanel)
		plt.draw()

		## all in one because splash occurs once and only once
		## modularize if u rly think necc but not rly lol

	def begin_screen(self):
		if self.dis_already == False: # ensure that image only gets added once to prev lag
			
			imageLocation = self.programImages[1]
			image = mpimg.imread(imageLocation)
			self.beginPanelTitle.imshow(image)

			imageLocation = self.programImages[2]
			image = mpimg.imread(imageLocation)
			self.beginPanelImg.imshow(image)
			plt.draw()

			self.dis_already = True

	def clear_begin_screen(self):
		self.beginPanelTitle.clear()
		self.beginPanelTitle.axis('off')

		#self.fig.delaxes(self.beginPanel) # DELETE SUBPLOT, sim. to clear, axis off
		self.beginPanelImg.clear()
		self.beginPanelImg.axis('off')
		plt.draw()

# =========================================
# 					LEAP MOTION LISTENER
# =========================================

class LeapListener(Leap.Listener):
	def on_init(self, controller):
		print 'Listener Added to Controller'

	def on_connect(self, controller):
		print 'LM: Device Connected'
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print 'LM" Device Disconnected'

	def on_device_failure(self, controller):
		print 'LM: Device Failed'

	def on_frame(self, controller):
		#CONSTANTLY CAPTURING, THIS IS THE MAIN LOOP
		#print 'LM: Frame Capturing' 
		game.game_loop()

# =========================================
# 								CONSTANTS
# =========================================

class Game():
	def __init__(self):
		
		# gui.setup_handPanel()

		# ------ GAME STATES -----------
		self.BEGIN = 0
		self.MENU = 1

		# ------ GLOBAL VARIABLES ------
		self.gameState = self.BEGIN ## to start

	def game_loop(self):

		frame = controller.frame()
		handPresent = len(frame.hands)

		if self.gameState == self.BEGIN:
			gui.begin_screen()

			# for gesture in frame.gestures():
			# 	if gesture.type == Leap.Gesture.TYPE_SWIPE:
			# 		print 'Swipe Detected'
			# 		gui.clear_begin_screen()

			if handPresent == 1:
				gui.clear_begin_screen()
				self.gameState = self.MENU

		elif self.gameState == self.MENU:
			gui.draw_hand(frame)

# =========================================
# 								MAIN SETUP
# =========================================

def main():
	print 'Press Enter to Quit...'

	# ------ GUTS ------------------

	# one time thing for aesthetics
	gui.setup_splashPanel()
	gui.splash_screen()

	gui.setup_beginPanel()
	gui.setup_handPanel()

	# then continue on with the MAIN GAME LOOP
	leapListener = LeapListener()
	controller.add_listener(leapListener)

	# ------ END PROGRAM -----------
	try:
		sys.stdin.readline()
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(leapListener)

# =========================================
# 								RUN PROGRAM
# =========================================

if __name__ == '__main__':
	controller = Leap.Controller()
	gui = GUI()
	game = Game()

	main()