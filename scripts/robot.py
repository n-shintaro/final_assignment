# coding:utf-8
#! /usr/bin/env python

"""
This file define the class "Robot"
"""

import rospy
import numpy as np
import math
from nav_msgs.msg import Odometry
from tf import transformations
from move_base_msgs.msg import MoveBaseActionGoal

class Robot:
    """
    A class used to represent an Robot
    ...
    Attributes
    ----------
    (x,y): float
        the position of robot
    (x_des,y_des): float
        target position of robot
    (vel_x, vel_y) : float
        velocity of robot
    yaw : float
        the yaw angle of the robot
    goal_flag: bool
        True: the robot reached the target position

    Methods
    -------
    clbk_odom
        When we subscribe the topic '/odom', we update the robot state(x, y, yaw).
    
    judge_goal
        Check if the robot is reaching the goal or not.

    send_destination
        Send the new target to the robot
    """

    def __init__(self):
        """
        Parameters
        -----------
        (x,y): float
        the position of robot
        (x_des,y_des): float
            target position of robot
        (vel_x, vel_y) : float
            velocity of robot
        yaw : float
            the yaw angle of the robot
        goal_flag: init
            1: the robot is reaching the target position
            0:the robot does not reaching the target position
        """
        self.x=0.0
        self.y=0.0
        self.x_des=0
        self.y_des=0
        self.vel_x=None
        self.vel_y=None
        self.yaw = 0
        self.goal_flag=0
        # publisher
        self.des_pub = rospy.Publisher('/move_base/goal',MoveBaseActionGoal, queue_size=10)
        # subscriber
        self.sub_odom = rospy.Subscriber('/odom', Odometry, self.clbk_odom)


    def clbk_odom(self,msg):
        """
        This is callback functon of "rospy.Subscriber('/odom', Odometry, self.clbk_odom)
        
        When we subscribe the topic '/odom', we update the robot state(x, y, yaw).
        And we save the data odom as the instance value of the class "robot".

        Parameters:
        ----------
        msg : Odemetry
            the odemetry data of the robot

        Returns:
        ----------
        None
        """
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
        """
        This is the function to check if the robot is reaching the goal or not.

        We consider the robot as reaching the goal when the distance between the robot and the target is below 0.8.
        When the robot is reaching the goal, the robot.goal_flag is chaged to 1

        Parameters:
        ----------
        None

        Returns:
        ----------
        None
        """
        err_pos = math.sqrt((self.y_des - self.y)**2 +(self.x_des - self.x)**2)
        print("t= %s" % rospy.get_time()+"-----------")
        print('destination position=['+str(self.x_des)+','+str(self.y_des)+"]")
        print('the current position=['+str(self.x)+','+str(self.y)+"]")
        print('the current yaw angle=['+str(self.yaw))
        print('distance to destination='+str(err_pos))

        if(err_pos < 0.8):
            print('reach goal!!!!!')
            self.goal_flag=1
    
    def send_destination(self):
        """
        This is the function to send the robot the new target

        We publish the information of the the target position of the robot to topic /move_base/goal.
        Message type is MoveBaseActionGoal

        Parameters:
        ----------
        None

        Returns:
        ----------
        None
        """

        print('send the target to the robot')
        move_base_action_goal=MoveBaseActionGoal()
        move_base_action_goal.goal.target_pose.header.frame_id="map"
        move_base_action_goal.goal.target_pose.pose.orientation.w=1
        move_base_action_goal.goal.target_pose.pose.position.x=self.x_des
        move_base_action_goal.goal.target_pose.pose.position.y=self.y_des
        print('des_x='+str(self.x_des))
        print('des_y='+str(self.y_des))
        self.des_pub.publish(move_base_action_goal)
