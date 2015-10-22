from pylab import *
import random
ion()
xPt = 0
yPt = 0
pt, = plot(xPt,yPt,'ko',markersize=20)
for i in arange(1,200):
    xPt = pt.get_xdata()
    xPt = xPt + (2.0*random.random()-1.0)*0.001
    pt.set_xdata(xPt)
    yPt = pt.get_ydata()
    yPt = yPt + (2.0*random.random()-1.0)*0.001
    pt.set_ydata(yPt)
    print xPt, yPt
    draw()
