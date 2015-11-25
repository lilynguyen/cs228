import Leap, sys, thread, time, random, timeit
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

listImages = ["./images/gesture0.png",
"./images/gesture1.png",
"./images/gesture2.png",
"./images/gesture3.png",
"./images/gesture4.png",
"./images/gesture5.png",
"./images/gesture6.png",
"./images/gesture7.png",
"./images/gesture8.png",
"./images/gesture9.png"]

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

totalTime = 0

redos = []

phase = 1

step = 0

digitString = 'digit'+str(rand)+'attempted'

if digitString not in userRecord:
  print digitString, 'not in database for', userName
  print 'Adding', digitString, 'to database for', userName
  userRecord[digitString] = 0
  pickle.dump(database, open('userData/database.p','wb'))

#print database

startTime = timeit.default_timer()
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

      if int(predictedGest) == rand:

        elapsed = timeit.default_timer() - startTime
        print "Time for Digit", rand, elapsed

        totalTime =+ elapsed

        userRecord[digitString+'Time'] = elapsed
        pickle.dump(database, open('userData/database.p','wb'))

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
          # print digitString, 'in database for', userName
          userRecord[digitString] += 1
          pickle.dump(database, open('userData/database.p','wb'))
          # print database

        #print database

        time.sleep(1)

        ClearGesturePanel()
        ClearCountPanel()

        if phase == 1:
          rand += 1

        if rand > 9:
          phase = 2
          # if the first run through of numbers is completed don't start at 0 again
          # start with the first digit that you took longer than avg on

          # retrieve the digits that took longer than average into a list
          # start with the first one and work through it

          for i in range(0,9):
            if userRecord['digit'+str(i)+'attemptedTime'] > (totalTime / 9):
              print 'Digit '+str(i)+' > AVG: '+str(totalTime / 9)
              redos.append(i)

        if phase == 2:
          print redos
          rand = redos[step]
          step += 1

        startTime = timeit.default_timer()

        digitString = 'digit'+str(rand)+'attempted'
        gesturePanel.imshow(mpimg.imread(listImages[rand]))

        if digitString not in userRecord:
          print digitString, 'not in database for', userName
          print 'Adding', digitString, 'to database for', userName
          userRecord[digitString] = 1
          pickle.dump(database, open('userData/database.p','wb'))
          # print database

        elif digitString in userRecord:
          # print digitString, 'in database for', userName
          userRecord[digitString] += 1
          pickle.dump(database, open('userData/database.p','wb'))
          # print database

        countPanel.text(0.5,0.5,userRecord[digitString],color='white',fontsize=15)