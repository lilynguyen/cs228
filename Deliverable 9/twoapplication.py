import Leap, sys, thread, time, random
import matplotlib, pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D


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

def ClearCountPanel():
  countPanel.clear()
  countPanel.axis("off")

def CenterData(testData):
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

def PredictData(testData):
  centeredData = CenterData(testData)
  #print clf.predict(centeredData)
  return clf.predict(centeredData)


database = pickle.load(open('userData/database.p','rb'))

userName = raw_input('Please enter your name: ')
userName = userName.lower()
formattedName = userName[0].upper() + userName[1:]

if userName in database:
  userRecord = database[userName]#['logins'] += 1
  userRecord['logins'] += 1
  print 'Welcome back ' + formattedName + '!'

elif userName not in database:
  database[userName] = {}
  userRecord = database[userName]
  userRecord['logins'] = 1
  print 'Welcome ' + formattedName + '!'

print database

pickle.dump(database, open('userData/database.p','wb'))

listImages = ["./images/0.png",
"./images/1.png",
"./images/2.png",
"./images/3.png",
"./images/4.png",
"./images/5.png",
"./images/6.png",
"./images/7.png",
"./images/8.png",
"./images/9.png"]

listDigits = ["./images/digit0.png",
"./images/digit1.png",
"./images/digit2.png",
"./images/digit3.png",
"./images/digit4.png",
"./images/digit5.png",
"./images/digit6.png",
"./images/digit7.png",
"./images/digit8.png", 
"./images/digit9.png"]

clf = pickle.load(open('userData/classifier.p','rb'))

testData = np.zeros((1,30),dtype='f')

controller = Leap.Controller()

matplotlib.interactive(True)
gs = gridspec.GridSpec(3,2)
fig = plt.figure(figsize=(8,6), facecolor="black")

#leapPanel
ax = fig.add_subplot(gs[:,0],projection='3d')
ax.set_xlim(-200,200)
ax.set_ylim(0,300)
ax.set_zlim(0,300)
ax.view_init(azim=90)
ax.axis("off")

motionPanel = fig.add_subplot(gs[0,1])
gesturePanel = fig.add_subplot(gs[1,1])

countPanel = fig.add_subplot(gs[2,1])

gesturePanel.axis("off")
motionPanel.axis("off")
countPanel.axis("off")

plt.draw()

rand = 0

phase = 1

digitString = 'digit'+str(rand)+'attempted'

if digitString not in userRecord:
  print digitString, 'not in database for', userName
  print 'Adding', digitString, 'to database for', userName
  userRecord[digitString] = 0
  pickle.dump(database, open('userData/database.p','wb'))

print database

gesturePanel.imshow(mpimg.imread(listImages[rand]))
countPanel.text(0.5,0.5,userRecord[digitString],color='white',fontsize=15)

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

      #print rand

      if int(predictedGest) == rand:
        ClearGesturePanel()
        ClearCountPanel()

        countPanel.text(0.5,0.5,str(userRecord[digitString])+" + 1",color='white',fontsize=15)
        gesturePanel.imshow(mpimg.imread("./images/check.png"))
        
        plt.draw()

        if digitString not in userRecord:
          print digitString, 'not in database for', userName
          print 'Adding', digitString, 'to database for', userName
          userRecord[digitString] = 1
          pickle.dump(database, open('userData/database.p','wb'))
          # print database

        elif digitString in userRecord:
          print digitString, 'in database for', userName
          userRecord[digitString] += 1
          pickle.dump(database, open('userData/database.p','wb'))
          # print database

        #print database

        time.sleep(1)

        ClearGesturePanel()
        ClearCountPanel()

        if rand < 9:
          rand += 1
        elif rand >= 9:
          phase = 2
          rand = 0

        digitString = 'digit'+str(rand)+'attempted'

        if phase == 1:
          gesturePanel.imshow(mpimg.imread(listImages[rand]))
        elif phase == 2:
          gesturePanel.imshow(mpimg.imread(listDigits[rand]))

        if digitString not in userRecord:
          print digitString, 'not in database for', userName
          print 'Adding', digitString, 'to database for', userName
          userRecord[digitString] = 1
          pickle.dump(database, open('userData/database.p','wb'))
          # print database

        elif digitString in userRecord:
          print digitString, 'in database for', userName
          userRecord[digitString] += 1
          pickle.dump(database, open('userData/database.p','wb'))
          # print database

        countPanel.text(0.5,0.5,userRecord[digitString],color='white',fontsize=15)