import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib

controller = Leap.Controller()

matplotlib.interactive(True)
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111,projection='3d')
plt.draw()

TYPE_INDEX = 1
TYPE_DISTAL = 3

# xMin = 1000.0
# xMax = -1000.0
# yMin = 1000.0
# yMax = -1000.0
# zMin = 1000.0
# zMax = -1000.0

while (True):
	frame = controller.frame()

	lines = []

	hands = frame.hands
	# print(len(hands))
	if len(hands): # If hands = 1, aka bool TRUE
		#print frame

		# want single hand
		hand = frame.hands[0]

		# iterate over each of the five fingers
		for i in range(0,5):

			# list of fingers in hand
			fingerList = hand.fingers

			finger = fingerList[i]

			# iterate through the four major bones
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

				lines.append(ax.plot([-xBase,-xTip],[zBase,zTip],[yBase,yTip],'r'))

		ax.set_xlim(-328.471557617,306.569793701)
		ax.set_ylim(43.1206054688,606.693664551)
		ax.set_zlim(-30.4142894745,511.524658203)

		ax.view_init(azim=90)

		# x = xTip
		# if (x < xMin):
		# 	xMin = x
		# if (x > xMax):
		# 	xMax = x

		# y = yTip
		# if (y < yMin):
		# 	yMin = y
		# if (y > yMax):
		# 	yMax = y

		# z = zTip
		# if (z < zMin):
		# 	zMin = z
		# if (z > zMax):
		# 	zMax = z

		# print xMin, xMax, yMin, yMax, zMin, zMax

		plt.draw()

		# # list of fingers in hand
		# fingerList = hand.fingers

		# # list of index fingers
		# indexFingerList = fingerList.finger_type(TYPE_INDEX)

		# # get the first index finger
		# indexFinger = indexFingerList[0]

		# # get distal joint
		# distalPhalangeOfIndexFinger = indexFinger.bone(TYPE_DISTAL)

		# # get TIP & BASE of joint
		# positionOfBoneTip = distalPhalangeOfIndexFinger.next_joint
		# positionOfBoneBase = distalPhalangeOfIndexFinger.prev_joint
		
		#print positionOfBoneTip, positionOfBoneBase

		# xTip = positionOfBoneTip[0]
		# yTip = positionOfBoneTip[1]
		# zTip = positionOfBoneTip[2]
		# xBase = positionOfBoneBase[0]
		# yBase = positionOfBoneBase[1]
		# zBase = positionOfBoneBase[2]

		# lines.append(ax.plot([xBase,xTip],[yBase,yTip],[zBase,zTip],'r'))
		# plt.draw()

		while (len(lines) > 0):
			ln = lines.pop()
			ln.pop(0).remove()
			del ln
			ln = []