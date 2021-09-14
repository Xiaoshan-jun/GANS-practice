# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 10:17:36 2021

@author: dekom
"""
import numpy as np
import matplotlib.pyplot as plt
import random
#f= open("vis/trajectory_vis.txt" ,"w+")
for i in range(200):
    x = np.zeros(16)
    y = np.zeros(16)
    #initial position, velocity, direction, curvature, 
    x_0 = random.uniform(-20, 20)
    y_0 = random.uniform(-20, 20)
    v = 1 #velocity
    a = random.randint(0,360)
    a_0 = a #direction
    delta_a = random.randint(-10, 10) #curvature
    for k in range(16):
        #calculate position at t+1
        a_1 = a_0 + delta_a
        x_1 = x_0 + v*np.cos(np.deg2rad(a_1))
        y_1 = y_0 + v*np.sin(np.deg2rad(a_1))
        #record position
        x[k] = x_1
        y[k] = y_1
        #update current position
        x_0 = x_1
        y_0 = y_1
        a_0 = a_1
    """
    # Draw point based on above x, y axis values.
    plt.scatter(x, y, s=10)
    # Set chart title.
    plt.title("trajectory " + "curvation: " + str(delta_a) +" initial direction: " + str(a))
    # Set x, y label text.
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-30, 30)
    plt.ylim(-30, 30)
    plt.grid(True)
    plt.show()
    """
    f= open("vis/trajectory%i_vis.txt" %i ,"w+")

    for j in range(len(x)):
        f.write(str(16*i + j))
        f.write('\t')
        f.write(str(i))
        f.write('\t')
        f.write(str(round(x[j],6)))
        f.write('\t')
        f.write(str(round(y[j],6)))
        f.write('\n')
    f.close()
    
