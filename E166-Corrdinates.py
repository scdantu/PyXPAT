'''
Created on Feb 8, 2012

@author: Dhakeneswar

import math
res=[]
from matplotlib.pyplot import *

subplot(211)
plot([1,2,3], label="test1")
plot([3,2,1], label="test2")
legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

subplot(223)
plot([1,2,3], label="test1")
plot([3,2,1], label="test2")
legend(bbox_to_anchor=(0., -0.225, 1., -0.225), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)


show()
'''
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(10)

fig = plt.figure()
ax = plt.subplot(111)

for i in xrange(5):
    line, = ax.plot(x, i * x, label='$y = %ix$'%i)

# Shink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.xlabel("X-axis")
plt.show()