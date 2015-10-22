import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
import time

class Reader:
	def __init__(self):

		self.lines = []
		matplotlib.interactive(True)
		self.fig = plt.figure(figsize=(8,6))
		self.ax = self.fig.add_subplot(111,projection='3d')

		# set dimensions for the 3D plane
		self.ax.set_xlim(-328.471557617,306.569793701)
		self.ax.set_ylim(43.1206054688,606.693664551)
		self.ax.set_zlim(-30.4142894745,511.524658203)

		# changes the view of the 3D plane
		self.ax.view_init(azim=90)

		# read total number of gestures saved in file
		f = open('userData/numOfGestures.dat','r')
		lineRead = f.readline()
		self.numberOfGesturesSaved = int(lineRead.rstrip())

		# Since the files start at 0, need to subtract 1 from the number of actual recorded gestures.
		# this reads the file's content of the 3d array
		# fileName = 'userData/gesture'+str(self.numberOfGesturesSaved-1)+'.dat' ### ONLY OPENEING THE LAST ONE
		# f = open(fileName,'r')
		# self.gestureData = np.load(f)
		# f.close()

	def PrintGesture(self,i):

		fileName = 'userData/gesture'+str(i)+'.dat'
		f = open(fileName,'r')
		gestureData = np.load(f)
		f.close()

		#gestureData = self.gestureData ####### STEP 36
		print gestureData

		for i in range(0,5):
			for j in range(0,4):
				xBase = gestureData[i,j,0]
				yBase = gestureData[i,j,1]
				zBase = gestureData[i,j,2]
				xTip = gestureData[i,j,3]
				yTip = gestureData[i,j,4]
				zTip = gestureData[i,j,5]
				
				self.lines.append(self.ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'b'))

		plt.draw() ######

		# Erases the lines so hand movements don't track
		while (len(self.lines) > 0):
			ln = self.lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []

		time.sleep(0.5)

	def PrintData(self):
		# from 0 to the number of gestures recorded previously
		for i in range(0, self.numberOfGesturesSaved):
			# print the gestures of each of those
			self.PrintGesture(i)

	def RunForever(self):
		while (True):
			self.PrintData()

reader = Reader()
reader.RunForever()

# NUMBER OF GESTURES SHOULD CORRESPOND TO THE NUMBER OF gesturei.dat FILES