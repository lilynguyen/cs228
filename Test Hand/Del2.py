import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import sys

controller = Leap.Controller()

matplotlib.interactive(True)
fig = plt.figure('signum',figsize=(8,6))
ax = fig.add_subplot(111,projection='3d',axisbg='none',frame_on=False)
ax.axis('off')
ax.view_init(azim=90)
ax.set_xlim(-50,50)
ax.set_ylim(150,200)
ax.set_zlim(400,550)

while (True):
	frame = controller.frame()
	lines = []
	hands = frame.hands
	if len(hands):
		hand = frame.hands[0]
		for i in range(0,5):
			fingerList = hand.fingers
			finger = fingerList[i]
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
				lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],color='b', lw=10, solid_capstyle='round'))
				

		plt.draw()
		while (len(lines) > 0):
			ln = lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []