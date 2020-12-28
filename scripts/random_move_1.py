#! /usr/bin/env python

# import ros stuff
import rospy
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import *
from robot import *
from final_assignment.srv import RandomPosition
from move_base_msgs.msg import MoveBaseActionGoal
import math

active_ = False
robot=Robot()

def random_move_switch(req):
    global active_
    active_ = req.data
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res

def move_random():
    global active_
    active_=False
    print('state1 : move randomly')
    set_target = rospy.ServiceProxy('/select_target', RandomPosition)
    response=set_target()
    robot.x_des=response.x
    robot.y_des=response.y
    robot.send_destination()

def main():
    global active_

    rospy.init_node('state1')
    
    srv = rospy.Service('/move_random', SetBool,random_move_switch)

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if not active_:
            continue
        else:
            robot.sub_odom
            move_random()
        rate.sleep()

if __name__ == '__main__':
    main()