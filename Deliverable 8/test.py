import Leap, sys, thread, time, random, matplotlib, pickle
import numpy as np
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()

image_file = cbook.get_sample_data('ada.png')
image = plt.imread(image_file)
plt.imshow(image)

plt.axis('off')
plt.show()