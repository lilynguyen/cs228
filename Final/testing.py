import sys
import os
import thread
import time

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from mpl_toolkits.mplot3d import Axes3D

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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
			'./images/gif.gif']

		# ------ GLOBAL VARIABLES ------
		self.lines = []

		# ------ WINDOW SETTINGS  ------
		mpl.interactive(True)
		mpl.rcParams['toolbar'] = 'None'
		self.fig = plt.figure(figsize=(15,10), facecolor='black')
		#self.fig.canvas.set_window_title('signum')

		# ------ PANEL INITS -----------
		self.splashPanel = ''
		self.beginPanel = ''
		self.handPanel = ''

	def setup_splashPanel(self):
		self.splashPanel = self.fig.add_subplot(111)
		self.splashPanel.axis('off')

	def setup_beginPanel(self):
		self.beginPanel = self.fig.add_subplot(111)
		self.beginPanel.axis('off')

	def setup_handPanel(self):
		self.handPanel = self.fig.add_subplot(111, projection='3d', axisbg='black', frame_on=False)
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
		imageLocation = self.positionImages[3]
		image = mpimg.imread(imageLocation)
		self.beginPanel.imshow(image)
		plt.draw()

	def clear_begin_screen(self):
		self.fig.delaxes(self.beginPanel) # DELETE SUBPLOT, sim. to clear, axis off
		# self.beginPanel.clear()
		# self.beginPanel.axis('off')
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
		#print 'LM: Frame Capturing' # CONSTANTLY CAPTURING, THIS IS THE LOOP
		game.game_loop()

# =========================================
# 								CONSTANTS
# =========================================

class Game():
	def __init__(self):
		
		gui.setup_handPanel()

		self.TRUE = 1
		self.FALSE = 0

		# ------ GAME STATES -----------
		self.BEGIN = 0
		self.DRAW_HAND = 1

		self.gameState = self.BEGIN ## to start

	def game_loop(self):
		frame = controller.frame()
		handPresent = len(frame.hands)

		if self.gameState == self.BEGIN:
			if handPresent == self.FALSE:
				gui.begin_screen()

			elif handPresent == self.TRUE:
				for gesture in frame.gestures():
					if gesture.type == Leap.Gesture.TYPE_SWIPE:
						gui.clear_begin_screen()
						self.gameState = self.DRAW_HAND


		elif self.gameState == self.DRAW_HAND:
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