import sys
import os
import thread
import threading
import time
import random
import Leap
import pickle
import numpy as np

from database import Database

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button
from threading import Timer

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec

# =========================================
# GUI CLASS ===============================
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
			'./images/gesture9.png'
		]

		self.digitImages = ['./images/digit0.png',
			'./images/digit1.png',
			'./images/digit2.png',
			'./images/digit3.png',
			'./images/digit4.png',
			'./images/digit5.png',
			'./images/digit6.png',
			'./images/digit7.png',
			'./images/digit8.png', 
			'./images/digit9.png'
		]

		self.statusImages = ['./images/check.png',
			'./images/wrong.png',
			'./images/0n.png', './images/0a.png',
			'./images/1n.png', './images/1a.png',
			'./images/2n.png', './images/2a.png',
			'./images/3n.png', './images/3a.png',
			'./images/4n.png', './images/4a.png',
			'./images/5n.png', './images/5a.png',
			'./images/6n.png', './images/6a.png',
			'./images/7n.png', './images/7a.png',
			'./images/8n.png', './images/8a.png',
			'./images/9n.png', './images/9a.png'
		]

		self.programImages = ['./images/logo.png',
			'./images/begin.png',
			'./images/exit.png',
			'./images/black.png', #3
			'./images/lvlsbg1.png', #4
			'./images/complvl1.png',
			'./images/lvl1bg.png', #6
			'./images/lvlsbg2.png', #7
			'./images/lvlsbg3.png', #8
			'./images/lvl2bg.png', #9
			'./images/lvl3bg.png', #10
			'./images/complvl2.png', #11
			'./images/complvl3.png' #12
			]

		self.badgeImages = ['./images/badge1.png',
			'./images/badge2.png',
			'./images/badge3.png',
			'./images/badge4.png'
		]

		# ------ GLOBAL VARIABLES ------
		self.lines = []

		self.begin_need_dis = True
		self.menu_need_dis = True
		self.lvl1_need_dis = True
		self.lvl2_need_dis = True
		self.lvl3_need_dis_rdy = True
		self.lvl3_need_dis = True
		self.exit_need_dis = True
		self.stat_need_dis = True

		self.prevGestNum = None

		# ------ WINDOW SETTINGS  ------
		mpl.interactive(True)
		mpl.rcParams['toolbar'] = 'None'
		self.fig = plt.figure('SIGNUM', figsize=(15,10), facecolor='black', tight_layout=True)
		#self.fig.canvas.set_window_title('signum')

		self.f = plt.figimage(mpimg.imread(self.programImages[3]))

		# ------ PANEL INITS -----------
		self.backgroundPanel = None
		self.gesturePanel = None
		self.digitPanel = None
		self.statusPanel = None
		self.handPanel = None

		self.badge1Panel = None
		self.badge2Panel = None
		self.badge3Panel = None
		self.badge4Panel = None

		self.badgeEarnedPanel = None

	def setup_backgroundPanel(self):
		self.backgroundPanel = self.fig.add_subplot(111)
		self.backgroundPanel.axis('off')

	def setup_gridspecs(self):
		gs = gridspec.GridSpec(4,10)

		self.gesturePanel = self.fig.add_subplot(gs[1,1])
		self.gesturePanel.axis('off')

		self.digitPanel = self.fig.add_subplot(gs[2,1])
		self.digitPanel.axis('off')

		self.statusPanel = self.fig.add_subplot(gs[1,8])
		self.statusPanel.axis('off')


		self.badge1Panel = self.fig.add_subplot(gs[3,3])
		self.badge1Panel.axis('off')

		self.badge2Panel = self.fig.add_subplot(gs[3,4])
		self.badge2Panel.axis('off')

		self.badge3Panel = self.fig.add_subplot(gs[3,5])
		self.badge3Panel.axis('off')

		self.badge4Panel = self.fig.add_subplot(gs[3,6])
		self.badge4Panel.axis('off')

		self.badgeEarnedPanel = self.fig.add_subplot(gs[1, 4:6])
		self.badgeEarnedPanel.axis('off')

	def setup_handPanel(self):
		self.handPanel = self.fig.add_subplot(111, projection='3d', axisbg='none', frame_on=False)
		self.handPanel.view_init(azim=90)
		self.handPanel.set_xlim(-50,50)
		self.handPanel.set_ylim(150,200)
		self.handPanel.set_zlim(400,550)
		self.handPanel.axis('off')

	def splash_screen(self):
		# all in one because splash occurs once and only once
		# modularize if u rly think necc but not rly lol

		# YO YOU CAN IMPLEMENT THIS AS A THREAD!

		imageLocation = self.programImages[0]
		image = mpimg.imread(imageLocation)
		self.backgroundPanel.imshow(image)
		# plt.figimage(image)
		plt.draw()

		time.sleep(2)

		self.backgroundPanel.clear()
		self.backgroundPanel.axis('off')

		plt.draw()

	def begin_screen(self):
		if self.begin_need_dis:
			imageLocation = self.programImages[1]
			image = mpimg.imread(imageLocation)
			self.backgroundPanel.imshow(image)
			# plt.figimage(image)
			plt.draw()

			self.begin_need_dis = False

	def clear_begin_screen(self):
		self.backgroundPanel.clear()
		self.backgroundPanel.axis('off')
		plt.draw()

	def menu_screen(self, latest_level):
		if self.menu_need_dis:

			self.f.remove()

			if latest_level == 1:
				imageLocation = self.programImages[4]
			elif latest_level == 2:
				imageLocation = self.programImages[7]
			elif latest_level == 3:
				imageLocation = self.programImages[8]
			elif latest_level == 4:
				imageLocation = self.programImages[8]

			image = mpimg.imread(imageLocation)
			self.f = plt.figimage(image)

			self.display_badges()

			self.menu_need_dis = False

	def display_badges(self):

		if db.get_badge1() == True:
			imageLocation=self.badgeImages[0]
			image = mpimg.imread(imageLocation)
			self.badge1Panel.imshow(image)

		if db.get_badge2() == True:
			imageLocation=self.badgeImages[1]
			image = mpimg.imread(imageLocation)
			self.badge2Panel.imshow(image)

		if db.get_badge3() == True:
			imageLocation=self.badgeImages[2]
			image = mpimg.imread(imageLocation)
			self.badge3Panel.imshow(image)

		# if db.get_badge4() == True:
		# 	imageLocation=self.badgeImages[3]
		# 	image = mpimg.imread(imageLocation)
		# 	self.badge4Panel.imshow(image)

	def clear_badges(self):
		self.badge1Panel.clear()
		self.badge1Panel.axis('off')

		self.badge2Panel.clear()
		self.badge2Panel.axis('off')

		self.badge3Panel.clear()
		self.badge3Panel.axis('off')

		self.badge4Panel.clear()
		self.badge4Panel.axis('off')

		plt.draw()

	def menu_choiceBar(self, progress):
		if progress == 75:
			c = 'k'
		elif progress < 75:
			c = 'b'
		self.lines.append(self.handPanel.plot([progress,75], [165,165], [450,450], \
			color=c, linewidth=10, solid_capstyle='round', ))

	def level_one_screen(self, gestureNum):
		if self.lvl1_need_dis:
			self.f.remove()
			self.clear_badges()

			imageLocation = self.programImages[6]
			image = mpimg.imread(imageLocation)
			self.f = plt.figimage(image)

			self.lvl1_need_dis = False

		# if the previous gesture number is different than this new call, change stuff
		if self.prevGestNum != gestureNum:
			imageLocation = self.gestureImages[gestureNum]
			image = mpimg.imread(imageLocation)
			self.gesturePanel.imshow(image)

			imageLocation = self.digitImages[gestureNum]
			image = mpimg.imread(imageLocation)
			self.digitPanel.imshow(image)

			self.prevGestNum = gestureNum

	def title_msg(self, phase):
		if phase == 1:
			string = 'Learn all the gestures!'
		elif phase == 2:
			string = 'Resign the gestures that took you longer!'
		elif phase == 3:
			string = 'Now try them all in random order!'
		elif phase == 0:
			string = 'Welcome ' + userNameFormatted + '!'
		elif phase == 4:
			string = 'Do you remember the signs of the digits?'
		elif phase == 5:
			string = 'Now try them all in random order!'
		elif phase == 6:
			string = 'Beat the clock! Sign as many gestures as you can!'

		self.handPanel.set_title(string, color="white", size="xx-large")

	def level_two_screen(self, gestureNum):
		if self.lvl2_need_dis:
			self.f.remove()
			self.clear_badges()

			imageLocation = self.programImages[9]
			image = mpimg.imread(imageLocation)
			self.f = plt.figimage(image)

			self.lvl2_need_dis = False

		# if the previous gesture number is different than this new call, change stuff
		if self.prevGestNum != gestureNum:
			imageLocation = self.digitImages[gestureNum]
			image = mpimg.imread(imageLocation)
			self.digitPanel.imshow(image)

			self.prevGestNum = gestureNum

	def level_three_screen_ready(self):
		if self.lvl3_need_dis_rdy:
			self.f.remove()
			self.clear_badges()

			imageLocation = self.programImages[10]
			image = mpimg.imread(imageLocation)
			self.f = plt.figimage(image)

			self.lvl3_need_dis_rdy = False

	def level_three_screen(self, gestureNum):
		if self.lvl3_need_dis:
			self.f.remove()
			self.clear_badges()

			imageLocation = self.programImages[10]
			image = mpimg.imread(imageLocation)
			self.f = plt.figimage(image)

			self.lvl3_need_dis = False

		# if the previous gesture number is different than this new call, change stuff
		if self.prevGestNum != gestureNum:
			imageLocation = self.digitImages[gestureNum]
			image = mpimg.imread(imageLocation)
			self.digitPanel.imshow(image)

			self.prevGestNum = gestureNum

	def clear_msg_hand(self):
		self.handPanel.set_title("")

	def clear_msg_bg(self):
		self.backgroundPanel.clear()
		self.backgroundPanel.axis('off')

	def text_msg(self, num):
		if num == 1:
			self.backgroundPanel.text(400, 165, 'You signed all the gestures once!', color='white', fontsize=20)
			self.backgroundPanel.text(450, 190, 'Unlocked Achievement 1', color='white', fontsize=20)

		elif num == 2:
			self.backgroundPanel.text(400, 165, 'You memorized all the signs by digit!', color='white', fontsize=20)
			self.backgroundPanel.text(450, 190, 'Unlocked Achievement 2', color='white', fontsize=20)

		elif num == 3:
			self.backgroundPanel.text(400, 165, 'You completed all the game levels!', color='white', fontsize=20)
			self.backgroundPanel.text(450, 190, 'Unlocked Achievement 3', color='white', fontsize=20)

	def lvl3_ready(self):
		self.backgroundPanel.text(520, 165, 'Get ready...', color='white', fontsize=20)
		plt.draw()

	def clear_badge_splash(self):
		self.badgeEarnedPanel.clear()
		self.badgeEarnedPanel.axis('off')

	def badge_splash(self, num):
		if num == 1:
			imageLocation=self.badgeImages[0]
			image = mpimg.imread(imageLocation)
			self.badgeEarnedPanel.imshow(image)

		elif num == 2:
			imageLocation=self.badgeImages[1]
			image = mpimg.imread(imageLocation)
			self.badgeEarnedPanel.imshow(image)

		elif num == 3:
			imageLocation=self.badgeImages[2]
			image = mpimg.imread(imageLocation)
			self.badgeEarnedPanel.imshow(image)
			plt.draw()

	def lvl_one_comp(self):
		self.clear_hand_tracing()
		self.f.remove()

		imageLocation = self.programImages[5]
		image = mpimg.imread(imageLocation)
		self.f = plt.figimage(image)

		plt.draw()

	def lvl_two_comp(self):
		self.clear_hand_tracing()
		self.f.remove()

		imageLocation = self.programImages[11]
		image = mpimg.imread(imageLocation)
		self.f = plt.figimage(image)

		plt.draw()

	def lvl_three_comp(self):
		self.clear_hand_tracing()
		self.f.remove()

		imageLocation = self.programImages[12]
		image = mpimg.imread(imageLocation)
		self.f = plt.figimage(image)

		plt.draw()

	def clear_gesturePanel(self):
		self.gesturePanel.clear()
		self.gesturePanel.axis('off')

	def clear_digitPanel(self):
		self.digitPanel.clear()
		self.digitPanel.axis('off')

	def update_statusPanel(self, phase):
		imageLocation = self.statusImages[phase]
		image = mpimg.imread(imageLocation)
		self.statusPanel.imshow(image)

	def clear_statusPanel(self):
		self.statusPanel.clear()
		self.statusPanel.axis('off')

	def draw_hand(self, frame, c):
		hands = frame.hands

		if len(hands):
			hand = frame.hands[0]

			for i in range(0,5):
				finger = hand.fingers[i]

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

					self.lines.append(self.handPanel.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip], \
						color=c, linewidth=25, solid_capstyle='round'))

		plt.draw() # SO IMPORTANT #
		self.clear_hand_tracing()

	def clear_hand_tracing(self):
		while (len(self.lines) > 0):
			ln = self.lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []

	def user_progressBar(self, progress):
		if progress >= 75:
			c = 'k'
		elif progress < 75:
			c = 'b'
		self.lines.append(self.handPanel.plot([progress,75], [165,165], [450,450], \
			color=c, linewidth=10, solid_capstyle='round', ))

	def timer_progressBar(self, time):
		if time == 75:
			c = 'k'
		elif time < 75:
			c = 'y'
		self.lines.append(self.handPanel.plot([time,75], [170,170], [450,450], \
			color=c, linewidth=10, solid_capstyle='round', ))

	# def gesture_status(self):
	# 	self.lines.append(self.handPanel.plot([],[150,150],[450,450]))

	def exit_screen(self):
		if self.exit_need_dis:
			self.clear_badges()
			self.clear_hand_tracing()
			self.f.remove()

			imageLocation = self.programImages[2]
			image = mpimg.imread(imageLocation)
			self.f = plt.figimage(image)

			plt.draw()

			self.exit_need_dis = False

	def stat_screen(self):
		if self.stat_need_dis:
			self.clear_badges()
			self.f.remove()

			imageLocation = self.programImages[3]
			image = mpimg.imread(imageLocation)
			self.f = plt.figimage(image)

			self.write_stats()

			plt.draw()

			self.stat_need_dis = False

	def write_stats(self):
		i = 0
		for record in db.userRecord:
			self.backgroundPanel.text(300, 10+i, record+' '+str(db.userRecord[record]), color='white', fontsize='9')
			i+= 20	

	def leaderboard_screen(self):
		self.f.remove()

		imageLocation = self.programImages[3]
		image = mpimg.imread(imageLocation)
		self.f = plt.figimage(image)

		self.write_leaderb()

		plt.draw()

	def write_leaderb(self):
		leaderb = db.get_leaderboard()
		self.backgroundPanel.text(300, 100, '1: '+leaderb[0]+' '+leaderb[1], color='white', fontsize='60')
		self.backgroundPanel.text(300, 200, '2: '+leaderb[2]+' '+leaderb[3], color='white', fontsize='60')
		self.backgroundPanel.text(300, 300, '3: '+leaderb[4]+' '+leaderb[5], color='white', fontsize='60')

# =========================================
# GAME CLASS ==============================
# =========================================

class Game():
	def __init__(self):

		# ------ GAME CONSTANTS -----------
		# Game States
		self.BEGIN = 0
		self.MENU = 1
		self.GAME_IN_PROGRESS = 3
		self.EXIT = 4
		self.STATS = 5

		# Menu States
		self.EXIT_VAL = 0
		self.LEVEL_1 = 1
		self.LEVEL_2 = 2
		self.LEVEL_3 = 3
		self.STATS_VAL = 9

		# Phase States
		self.PHASE_1 = 1
		self.PHASE_2 = 2
		self.PHASE_3 = 3 
		self.PHASE_OVER = 4

		# Gesture Correct/Incorrect
		self.CHECK = 0
		self.WRONG = 1

		# Progress Bar Params
		self.RESTART = 75
		self.END = -75

		# ------ GLOBAL VARIABLES ------
		self.testData = np.zeros((1,30),dtype='f')
		self.gameState = self.BEGIN ## to start
		self.gameLvl = None
		self.levelPhase = self.PHASE_1
		self.resetStartTime = True
		self.start_level = True
		self.startTime = 0
		self.onTrack = None
		self.prevGestNum = None

		self.gestureNum = 0
		self.time = self.RESTART
		self.progress = self.RESTART

		self.roundPoints = 0
		self.lives = 3

		self.trialTime = 0
		self.gestureTime = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
		self.redoList = []

	def game_loop(self):
		frame = controller.frame()
		hands_in_frame = len(frame.hands)
		self.gather_testData(frame) # constantly reading hand

	# ========================
	# GAME STATE PROCESS =====
	# ========================

		if self.gameState == self.BEGIN:
			gui.begin_screen()
			if hands_in_frame == 1: ## WHERE SWIPE WOULD GO 
				gui.clear_begin_screen()
				self.gameState = self.MENU

		elif self.gameState == self.MENU:

			thread.start_new_thread(gui.title_msg, (0,)) #####

			gui.draw_hand(frame, '#ffffff')
			gui.menu_screen(db.latest_level())
			gui.menu_choiceBar(self.progress)

			if hands_in_frame == 1:
				predictedGesture = self.predict_data(self.testData)

				if int(predictedGesture) == self.LEVEL_1:
					self.onTrack = self.LEVEL_1
					self.progress -= 10 ## this is the incrementer...the timer
					if self.progress <= self.END:
						print 'ENTER LEVEL 1'
						self.gameState = self.GAME_IN_PROGRESS
						self.gameLvl = self.LEVEL_1
						self.progress = self.RESTART

				elif int(predictedGesture) == self.LEVEL_2:
					self.onTrack = self.LEVEL_2
					self.progress -= 10
					if self.progress <= self.END:
						print 'ENTER LEVEL 2'
						self.gameState = self.GAME_IN_PROGRESS
						self.gameLvl = self.LEVEL_2
						self.progress = self.RESTART

				elif int(predictedGesture) == self.LEVEL_3:
					self.onTrack = self.LEVEL_3
					self.progress -= 10
					if self.progress <= self.END:
						print 'ENTER LEVEL 3'
						self.gameState = self.GAME_IN_PROGRESS
						self.gameLvl = self.LEVEL_3
						self.progress = self.RESTART

				elif int(predictedGesture) == self.EXIT_VAL:
					self.onTrack = self.EXIT_VAL
					self.progress -= 10
					if self.progress <= self.END:
						print 'ENTER EXIT'
						self.gameState = self.EXIT

				elif int(predictedGesture) == self.STATS_VAL:
					self.onTrack = self.STATS_VAL
					self.progress -= 10
					if self.progress <= self.END:
						print 'ENTER STATS'
						self.gameState = self.STATS

				if int(predictedGesture) != self.onTrack: # ENFORCES HOLD
					self.progress = self.RESTART

			else: # if hand leaves frame, more than one hand in frame
				self.progress = self.RESTART

		elif self.gameState == self.GAME_IN_PROGRESS:
			predictedGesture = self.predict_data(self.testData)

		# ================
		# LEVEL 1 ========
		# ================

			if self.gameLvl == self.LEVEL_1:

				if int(predictedGesture) == self.gestureNum:
					gui.draw_hand(frame,'green')
				else:
					gui.draw_hand(frame,'red')

				gui.level_one_screen(self.gestureNum)
				gui.user_progressBar(self.progress)

				if self.resetStartTime:
					self.startTime = time.time()
					self.resetStartTime = False

				if self.levelPhase == self.PHASE_1:

					self.msg(1)

					if hands_in_frame == 1:
						if int(predictedGesture) == self.gestureNum:
							self.progress -= 10

							if self.progress <= self.END:
								thread.start_new_thread(self.correct, ())
								gui.clear_gesturePanel()
								gui.clear_digitPanel()

								elapsed = time.time() - self.startTime

								self.gestureTime[self.gestureNum] = elapsed

								db.add_time(self.gestureNum, elapsed)
								db.add_attempt(self.gestureNum)

								self.progress = self.RESTART
								self.resetStartTime = True

								if self.gestureNum < 9:
									self.gestureNum += 1

								elif self.gestureNum == 9: #SETUP FOR PHASE 2

									db.earn_badge1()
									thread.start_new_thread(self.badges, (1,))

									for i in self.gestureTime: # i = gestNum
										self.trialTime += self.gestureTime[i]
									for i in self.gestureTime:
										if self.gestureTime[i] > (self.trialTime/10): # find the gests that took you too long...
											self.redoList.append(i)

									self.gestureNum = self.redoList[0]
									self.levelPhase = self.PHASE_2
									print 'ENTER PHASE 2'

					else:
						self.progress = self.RESTART

				elif self.levelPhase == self.PHASE_2:

					self.msg(2)
					
					if hands_in_frame == 1:
						if int(predictedGesture) == self.gestureNum:
							self.progress -= 10

							if self.progress <= self.END:
								thread.start_new_thread(self.correct, ())
								gui.clear_gesturePanel()
								gui.clear_digitPanel()

								elapsed = time.time() - self.startTime

								db.add_time(self.gestureNum, elapsed)
								db.add_attempt(self.gestureNum)

								self.progress = self.RESTART
								self.resetStartTime = True

								self.redoList.remove(self.redoList[0])

								if len(self.redoList) > 0:
									self.gestureNum = self.redoList[0]

								elif len(self.redoList) == 0: # SETUP FOR 3
									self.prevGestNum = self.gestureNum
									self.gestureNum = random.randint(0,9)
									while self.prevGestNum == self.gestureNum:
										self.gestureNum = random.randint(0,9)

									self.redoList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
									self.levelPhase = self.PHASE_3
									print 'ENTER PHASE 3'

					else:
						self.progress = self.RESTART

				elif self.levelPhase == self.PHASE_3:

					self.msg(3)
					
					if hands_in_frame == 1:
						if int(predictedGesture) == self.gestureNum:
							self.progress -= 10

							if self.progress <= self.END:
								thread.start_new_thread(self.correct, ())
								gui.clear_gesturePanel()
								gui.clear_digitPanel()

								elapsed = time.time() - self.startTime

								db.add_time(self.gestureNum, elapsed)
								db.add_attempt(self.gestureNum)

								self.progress = self.RESTART
								self.resetStartTime = True

								self.redoList.remove(self.gestureNum)

								if len(self.redoList) > 0:
									randomIndex = random.randint(0,len(self.redoList)-1)
									self.gestureNum = self.redoList[randomIndex]

								elif len(self.redoList) == 0:
									self.param_resets()

									db.completed_lvl1()

									self.fin_lvl1()
									self.gameState = self.MENU
									gui.menu_need_dis = True
									gui.lvl1_need_dis = True
									print 'MAIN MENU'

					else:
						self.progress = self.RESTART



		# ================
		# LEVEL 2 ========
		# ================

			elif self.gameLvl == self.LEVEL_2:

				if int(predictedGesture) == self.gestureNum:
					gui.draw_hand(frame,'green')
				else:
					gui.draw_hand(frame,'red')

				gui.level_two_screen(self.gestureNum)
				gui.user_progressBar(self.progress)

				if self.resetStartTime:
					self.startTime = time.time()
					self.resetStartTime = False

				if self.levelPhase == self.PHASE_1:

					self.msg(4)

					if hands_in_frame == 1:
						if int(predictedGesture) == self.gestureNum:
							self.progress -= 10

							if self.progress <= self.END:
								thread.start_new_thread(self.correct, ())
								gui.clear_digitPanel()

								elapsed = time.time() - self.startTime

								db.add_time(self.gestureNum, elapsed)
								db.add_attempt(self.gestureNum)

								self.progress = self.RESTART
								self.resetStartTime = True

								if self.gestureNum < 9:
									self.gestureNum += 1

								elif self.gestureNum == 9:

									db.earn_badge2()
									thread.start_new_thread(self.badges, (2,))

									self.gestureNum = random.randint(0,(9-1)) #exclude 9 from being generated first DO THIS FOR LVL1
									self.redoList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
									self.levelPhase = self.PHASE_2
									print 'ENTER PHASE 2'

					else:
						self.progress = self.RESTART

				elif self.levelPhase == self.PHASE_2:
					
					self.msg(5)

					if hands_in_frame == 1:
						if int(predictedGesture) == self.gestureNum:
							self.progress -= 10

							if self.progress <= self.END:
								thread.start_new_thread(self.correct, ())
								gui.clear_digitPanel()

								db.add_attempt(self.gestureNum)

								self.progress = self.RESTART

								self.redoList.remove(self.gestureNum)

								if len(self.redoList) > 0:
									randomIndex = random.randint(0, len(self.redoList)-1)
									self.gestureNum = self.redoList[randomIndex]
 
								elif len(self.redoList) == 0:
									self.param_resets()

									db.completed_lvl2()

									self.fin_lvl2()
									self.gameState = self.MENU
									gui.menu_need_dis = True
									gui.lvl2_need_dis = True
									print 'MAIN MENU'

		# ================
		# LEVEL 3 ========
		# ================

			elif self.gameLvl == self.LEVEL_3:

				gui.level_three_screen_ready()
				self.msg(6)

				if int(predictedGesture) == self.gestureNum:
					gui.draw_hand(frame,'green')
				else:
					gui.draw_hand(frame,'red')

				if self.start_level:
					self.msg_lvl3()
					self.gestureNum = random.randint(0,9)
					self.start_level = False

				gui.level_three_screen(self.gestureNum)
				gui.user_progressBar(self.progress)
				gui.timer_progressBar(self.time)

				if self.levelPhase == self.PHASE_1:
					if self.lives == 0:
						self.levelPhase = self.PHASE_OVER
						print 'ENTER PHASE OVER'

					if self.time > self.END:
						self.time -= 5

						if hands_in_frame == 1:
							if int(predictedGesture) == self.gestureNum:
								self.progress -= 10

								if self.progress <= self.END:
									thread.start_new_thread(self.correct, ())
									gui.clear_digitPanel()

									db.add_attempt(self.gestureNum)

									self.roundPoints += 1

									self.progress = self.RESTART
									self.time = self.RESTART

									self.prevGestNum = self.gestureNum
									self.gestureNum = random.randint(0,9)
									while self.prevGestNum == self.gestureNum:
										self.gestureNum = random.randint(0,9)

							else:
								if self.progress < self.RESTART:
									self.progress += 3
						else:
								if self.progress < self.RESTART:
									self.progress += 3

					elif self.time <= self.END:
						thread.start_new_thread(self.wrong, ())
						gui.clear_digitPanel()

						self.progress = self.RESTART
						self.time = self.RESTART

						self.lives -= 1

						self.prevGestNum = self.gestureNum
						self.gestureNum = random.randint(0,9)
						while self.prevGestNum == self.gestureNum:
							self.gestureNum = random.randint(0,9)		

				elif self.levelPhase == self.PHASE_OVER:
					gui.clear_digitPanel()
					self.param_resets()

					db.add_score(self.roundPoints)

					db.earn_badge3()
					self.badges(3)

					db.completed_lvl3()

					self.fin_lvl3()

					self.leaderboard()

					self.gameState = self.MENU
					gui.menu_need_dis = True
					gui.lvl3_need_dis_rdy = True
					gui.lvl3_need_dis = True
					print 'MAIN MENU'
					

		elif self.gameState == self.EXIT:
			self.exit_game()

		elif self.gameState == self.STATS:
			gui.draw_hand(frame, '#ffffff') # should incorporate use of going back to the menu!
			self.stats_view()

	def correct(self):
		gui.update_statusPanel(self.CHECK)
		time.sleep(2)
		gui.clear_statusPanel()

	def wrong(self):
		gui.update_statusPanel(self.WRONG)
		time.sleep(2)
		gui.clear_statusPanel()

	def msg(self, phase):
		gui.title_msg(phase)

	def leaderboard(self):
		gui.leaderboard_screen()
		time.sleep(5)
		gui.clear_msg_bg()

	def msg_lvl3(self):
		gui.lvl3_ready()
		time.sleep(4)
		gui.clear_msg_bg()

	def fin_lvl1(self):
		gui.clear_statusPanel()
		gui.clear_msg_hand()
		gui.lvl_one_comp()
		time.sleep(2)

	def fin_lvl2(self):
		gui.clear_statusPanel()
		gui.clear_msg_hand()
		gui.lvl_two_comp()
		time.sleep(2)

	def fin_lvl3(self):
		gui.clear_statusPanel()
		# gui.clear_digitPanel()
		gui.clear_msg_hand()
		gui.lvl_three_comp()
		time.sleep(2)

	def exit_game(self):
		gui.clear_msg_hand()
		gui.exit_screen()
		time.sleep(2)
		plt.close()
		# PRESS ENTER TO QUIT

	def stats_view(self):
		gui.clear_msg_hand()
		gui.stat_screen()

	def param_resets(self):
		self.gestureNum = 0
		self.levelPhase = self.PHASE_1
		self.trialTime = 0
		self.resetStartTime = True

	def badges(self, num):
		gui.text_msg(num)
		gui.badge_splash(num)
		time.sleep(4)
		gui.clear_msg_bg()
		gui.clear_badge_splash()

	def center_data(self, testData):
	  allXCoordinates = self.testData[0,::3]
	  meanValue = allXCoordinates.mean()
	  self.testData[0,::3] = allXCoordinates - meanValue

	  allYCoordinates = self.testData[0,1::3]
	  meanValue = allYCoordinates.mean()
	  self.testData[0,1::3] = allYCoordinates - meanValue

	  allZCoordinates = self.testData[0,2::3]
	  meanValue = allZCoordinates.mean()
	  self.testData[0,2::3] = allZCoordinates - meanValue
	  return self.testData

	def predict_data(self, testData):
		centeredData = self.center_data(testData)
		predictedGesture = clf.predict(centeredData)
		return predictedGesture

	def gather_testData(self, frame):
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

				if ((j == 0) | (j == 3)):
					self.testData[0,k] = xTip
					self.testData[0,k+1] = yTip
					self.testData[0,k+2] = zTip
					k = k + 3

# =========================================
# MAIN SETUP ==============================
# =========================================

def main():
	print 'Press Enter to Quit...'

	# ------ GUTS ------------------
	# userName = get_username()
	# db = Database(userName, dbFile)
	userExists = db.user_exists()
	# userNameFormatted = get_formatted_username(userName)

	if userExists:
		db.add_login()
		print('Welcome back ' + userNameFormatted + '!')
	else:
		db.create_profile()
		db.add_login()
		print('Welcome ' + userNameFormatted + '!')

	##############

	db.display_profile()
	db.get_leaderboard()

	##############

	gui.setup_backgroundPanel()

	gui.splash_screen()

	gui.setup_gridspecs()
	gui.setup_handPanel()

	# then continue on with the MAIN GAME LOOP
	leapListener = LeapListener()
	controller.add_listener(leapListener)

	# ------ END PROGRAM -----------
	try:
		sys.stdin.readline() # change this to control how program ends
	except KeyboardInterrupt:
		pass
	finally:
		controller.remove_listener(leapListener)

# =========================================
# MOD LVL FCNS ============================
# =========================================

def get_username():
	# userName = raw_input('Enter Name: ')
	userName = 'LILY'
	userNameLower = userName.lower()
	return userNameLower

def get_formatted_username(userName):
	userNameFormatted = userName[0].upper() + userName[1:]
	return userNameFormatted


# =========================================
# LEAP MOTION LISTENER ====================
# =========================================

class LeapListener(Leap.Listener):
	def on_init(self, controller):
		print 'Listener Added to Controller'

	def on_connect(self, controller):
		print 'Leap Motion Device Connected'
		controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
		controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
		controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		print 'Leap Motion Device Disconnected'

	def on_device_failure(self, controller):
		print 'Leap Motion Device Failed'

	def on_frame(self, controller):
		#CONSTANTLY CAPTURING, THIS IS THE MAIN LOOP
		#print 'Leap Motion Frame Capturing' 
		game.game_loop()

# =========================================
# RUN PROGRAM =============================
# =========================================

if __name__ == '__main__':
	dbFile = pickle.load(open('userData/database.p','rb'))
	clf = pickle.load(open('userData/classifier.p','rb'))

	controller = Leap.Controller()
	gui = GUI()
	game = Game()

	userName = get_username() #
	userNameFormatted = get_formatted_username(userName) #
	db = Database(userName, dbFile) #

	main()