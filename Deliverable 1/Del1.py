# If lib contents are not contained in the same folder, this will not run.

from pylab import *

import random

import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class SampleListener(Leap.Listener):

    TYPE_INDEX = 1
    TYPE_DISTAL = 3
    
    xMin = 1000.0
    xMax = -1000.0
    yMin = 1000.0
    yMax = -1000.0

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):        
        frame = controller.frame()
        hands = frame.hands
        
        if(len(frame.hands) > 0):
            #print "hand detected."
            for i in arange(1,2):
                
                # Want to use the first and only hand in a frame
                hand = frame.hands[0] #HAND LIST

                # get fingers...based on IDs...new hand in frame is different
                fingerList = hand.fingers #FINGER LIST

                # list of index fingers
                indexFingerList = fingerList.finger_type(self.TYPE_INDEX) #FINGER LIST

                # get the only index finger in the hand
                indexFinger = indexFingerList[0] #FINGER
                
                # gets the bone of the finger
                distalPhalange = indexFinger.bone(self.TYPE_DISTAL) #BONE

                # get VECTOR of bone joint position (x, y, z)
                distalPhalangePosition = distalPhalange.next_joint #VECTOR

                # print coordinates
                print distalPhalangePosition

                # set the fingy coords
                pt.set_xdata(distalPhalangePosition.x)
                pt.set_ydata(distalPhalangePosition.y)

                # Finding appropriate axis sizes, finds limits based on stretch of fingy leap mo
##                x = distalPhalangePosition.x
##                if (x < self.xMin):
##                    self.xMin = x
##                if (x > self.xMax):
##                    self.xMax = x
##                    
##                y = distalPhalangePosition.y
##                if (y < self.yMin):
##                    self.yMin = y
##                if (y > self.yMax):
##                    self.yMax = y
##
##                print "xMIN",self.xMin,"xMAX",self.xMax,"yMIN", self.yMin, "yMAX", self.yMax
                
                draw()
        #else:
            #print "hand not detected."
 
def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-356.74319458,+385.231842041)
ax.set_ylim(23.7192516327,+530.87902832)
xPt = 0
yPt = 0
pt, = plot(xPt,yPt,'ko',markersize=20)

if __name__ == "__main__":    
    main()
