# coding:utf-8
#! /usr/bin/env python

import rospy
import numpy as np
import math

"""
A class used to represent an Robot

...
Attributes
----------
(x,y): float 
    the position of robot

(x_t,y_t): float 
    target position of robot

(vel_x, vel_y) : float
    velocity of robot

goal_flag: bool
    True: the robot reached the target position

k:constant of proportionality


Methods
-------
update_state
    Update the robot position and velocity.
"""

class Robot:
    """
    Parameters
    ----------
    name : str
    ...
    The name of the animal
    sound : str
    Attributes
    The sound the animal makes
    ----------
    num_legs : int, optional
    says_str : str
    The number of legs the animal (default is 4)
    a formatted string to print out what the animal says
    """

    def __init__(self):
        self.x=0.0
        self.y=0.0
        self.x_des=0
        self.y_des=0
        self.vel_x=None
        self.vel_y=None
        self.yaw_ = 0
