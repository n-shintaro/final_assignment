#! /usr/bin/env python

# import ros stuff

"""
    This is the file to make the robot move as the state 2.
    when the service "/user_input" is called.

        -state 2:
            directly ask the user of the next target position
            (checking that the position is one of the possible six)

"""

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
    """
    This is callback function of the server of service "/user_input".
    Change the mode to 1 in order to ask user to decide the target position.

    Parameters:
        ----------
        req :SetBool

        Returns:
        ----------
        res :SetBoolResponse
        return res.success = True  and res.message = 'Done!'
    """
    global mode_
    mode_ = 1
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res

def user_input():
    """
    This is function to ask user
    to choose 1 out of 6 possible target positions from [(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)]
    
    This input data is saved as the instance value of robot (instance) 
    and send the target position to the robot.
    Change the mode to 2.

    Parameters:
        ----------
        None

        Returns:
        ----------
        None
    """

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
    # check whether the input data is one of the possible target positions.
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
    """
    This is main function and decide the robot motion depending on the mode of the robot.

    mode_=0: This node don't do anything.
    mode_=1: This node ask the user to decide the target position.
    mode_=2: The robot is moving to the target.
            This node subscribe the odom and check weather the robot is reaching the target.
            If the robot is reaching the goal, send this service as the client "rospy.ServiceProxy("/reach_goal",SetBool)"
    
    Parameters:
        ----------
        None

        Returns:
        ----------
        None

    """

    global mode_

    rospy.init_node('state2')
    
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