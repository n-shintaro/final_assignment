#! /usr/bin/env python

# import ros stuff
import rospy
from nav_msgs.msg import Odometry
from tf import transformations
from std_srvs.srv import Empty,EmptyResponse
from std_srvs.srv import *
from robot import *
from final_assignment.srv import RandomPosition
from move_base_msgs.msg import MoveBaseActionGoal
import math

mode_ = 0
robot=Robot()

def random_move_switch(req):
    global mode_
    mode_ = 1
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res

def send_target_pos():
    global mode_
    print('state1 : move randomly')
    set_target = rospy.ServiceProxy('/select_target', RandomPosition)
    response=set_target()
    robot.x_des=response.x
    robot.y_des=response.y
    robot.send_destination()
    mode_=2

def main():
    global mode_

    rospy.init_node('state1')
    
    reach_goal_srv = rospy.ServiceProxy("/reach_goal",SetBool)

    srv = rospy.Service('/move_random', SetBool,random_move_switch)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        print('mode='+str(mode_))
        if mode_==0:
            rate.sleep()
            continue
        elif mode_==1:
            send_target_pos()
        elif mode_==2:
            robot.sub_odom
            robot.judge_goal()
            if robot.goal_flag==1:
                mode_=0
                response=reach_goal_srv(True)
        else:
            rospy.logerr('Unknown state!')
        rate.sleep()

if __name__ == '__main__':
    main()