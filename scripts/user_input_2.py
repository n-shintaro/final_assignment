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

def user_input_switch(req):
    global mode_
    mode_ = 1
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res

def user_input():
    print('state2 : user input the destination')
    candidate_des_pos_x=[-4,-4,-4,5,5,5]
    candidate_des_pos_y=[-3,2,7,-7,-3,1]
    candidate_des_pos=[(-4,-3),(-4,2),(-4,7),(5,-7),(5,-3),(5,1)]
    print("Please insert a new state from "+str(candidate_des_pos))
    try:
        des_x = float(raw_input('des_pos_x :'))
        des_y =float(raw_input('des_pos_y :'))
    except:
        print("an error occurred")
        return user_input()
    if (des_x,des_y) in candidate_des_pos:
        print("Thanks! Let's change the des")
        robot.x_des=des_x
        robot.y_des=des_y
        global mode_
        mode_=2
        robot.send_destination()
    else:
        print("value is invalid.\n You should choose from"+str(candidate_des_pos))
        return user_input()


def main():
    global mode_

    rospy.init_node('state1')
    
    reach_goal_srv = rospy.ServiceProxy("/reach_goal",SetBool)

    srv = rospy.Service('/user_input', SetBool,user_input_switch)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if mode_==0:
            rate.sleep()
            continue
        elif mode_==1:
            user_input()
        elif mode_==2:
            robot.sub_odom
            robot.judge_goal()
            if robot.goal_flag==1:
                response=reach_goal_srv(True)
                mode_=0
                robot.goal_flag=0
        else:
            rospy.logerr('Unknown state!')
        rate.sleep()

if __name__ == '__main__':
    main()