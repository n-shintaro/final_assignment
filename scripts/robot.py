# coding:utf-8
#! /usr/bin/env python

import rospy
import numpy as np
import math
from nav_msgs.msg import Odometry
from tf import transformations
from move_base_msgs.msg import MoveBaseActionGoal


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

        self.des_pub = rospy.Publisher('/move_base/goal',MoveBaseActionGoal, queue_size=10)
        self.sub_odom = rospy.Subscriber('/odom', Odometry, self.clbk_odom)
    
    def clbk_odom(self,msg):
        # position
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        # yaw
        quaternion = (
            msg.pose.pose.orientation.x,
            msg.pose.pose.orientation.y,
            msg.pose.pose.orientation.z,
            msg.pose.pose.orientation.w)
        euler = transformations.euler_from_quaternion(quaternion)
        self.yaw = euler[2]

    def judge_goal(self):
        err_pos = math.sqrt((self.y_des - self.y)**2 +(self.x_des - self.x)**2)
        print('err_pos='+str(err_pos))
        if(err_pos < 1.0):
            print('reach goal!!!!!')
            print('des_x='+str(self.x_des))
            print('des_y='+str(self.y_des))
            print('x='+str(self.x))
            print('y='+str(self.y))
    
    def send_destination(self):
        print('send the destination to the robot')
        move_base_action_goal=MoveBaseActionGoal()
        move_base_action_goal.goal.target_pose.header.frame_id="map"
        move_base_action_goal.goal.target_pose.pose.orientation.w=1
        move_base_action_goal.goal.target_pose.pose.position.x=self.x_des
        move_base_action_goal.goal.target_pose.pose.position.y=self.y_des
        print('des_x='+str(self.x_des))
        print('des_y='+str(self.y_des))
        self.des_pub.publish(move_base_action_goal)
