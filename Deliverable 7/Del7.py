import Leap, sys, thread, time, random
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import pickle
import numpy as np

def DrawMotion():
  plt.draw()
  while (len(lines) > 0):
    ln = lines.pop()
    ln.pop(0).remove()
    del ln
    ln = []

def ClearMotionPanel():
  motionPanel.clear()
  motionPanel.axis("off")

def ClearGesturePanel():
  gesturePanel.clear()
  gesturePanel.axis("off")

def CenterData(tD):
  allXCoordinates = tD[0,::3]
  meanValue = allXCoordinates.mean()
  tD[0,::3] = allXCoordinates - meanValue

  allYCoordinates = tD[0,1::3]
  meanValue = allYCoordinates.mean()
  tD[0,1::3] = allYCoordinates - meanValue

  allZCoordinates = tD[0,2::3]
  meanValue = allZCoordinates.mean()
  tD[0,2::3] = allZCoordinates - meanValue
  return tD

def PredictData(tD):
  centeredData = CenterData(tD)
  print clf.predict(centeredData)
  return clf.predict(centeredData)


listImages = ["./images/0.png","./images/1.png","./images/2.png","./images/3.png","./images/4.png","./images/5.png","./images/6.png","./images/7.png","./images/8.png","./images/9.png"]

clf = pickle.load(open('userData/classifier.p','rb'))

testData = np.zeros((1,30),dtype='f')

controller = Leap.Controller()

matplotlib.interactive(True)
gs = gridspec.GridSpec(2,2)
fig = plt.figure(figsize=(8,6), facecolor="black")

#leapPanel
ax = fig.add_subplot(gs[:,:-1],projection='3d')
ax.set_xlim(-200,200)
ax.set_ylim(0,300)
ax.set_zlim(0,300)
ax.view_init(azim=90)
ax.axis("off")

motionPanel = fig.add_subplot(gs[:-1,-1])
gesturePanel = fig.add_subplot(gs[-1,-1])

gesturePanel.axis("off")
motionPanel.axis("off")

plt.draw()

rand = random.randint(0,9)
gesturePanel.imshow(mpimg.imread(listImages[rand]))

while (True):
  frame = controller.frame()
  lines = []

  k = 0
  hand = frame.hands[0]

  for i in range(0,5):
    finger =  hand.fingers[i]

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

  DrawMotion()
  
  if len(frame.hands) == 0:
    gameState = 0
    ClearMotionPanel()
    motionPanel.imshow(mpimg.imread("./images/over.png"))

  elif len(frame.hands) == 1:
    if min(testData[0,0::3]) < -100:
      gameState = 1
      ClearMotionPanel()
      motionPanel.imshow(mpimg.imread("./images/left.png"))

    elif max(testData[0,0::3]) > 100:
      gameState = 1
      ClearMotionPanel()
      motionPanel.imshow(mpimg.imread("./images/right.png"))

    elif (min(testData[0,::3]) > -100) and (max(testData[0,::3]) < 100):
      gameState = 2
      ClearMotionPanel()
      motionPanel.imshow(mpimg.imread("./images/centered.png"))

      predictedGest = PredictData(testData)

      print rand
      if int(predictedGest) == rand:
        ClearGesturePanel()
        gesturePanel.imshow(mpimg.imread("./images/check.png"))
        plt.draw()
        time.sleep(1)

        ClearGesturePanel()
        rand = random.randint(0,9)
        gesturePanel.imshow(mpimg.imread(listImages[rand]))