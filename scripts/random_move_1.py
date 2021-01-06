#! /usr/bin/env python

# import ros stuff

"""
    This is the file to make the robot move as the state 1.
    when the service "move_random" is called.

        -state 1:
            move randomly in the environment, by choosing 1 out of 6 possible target positions:
            [(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)], implementing a random position service.

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

# mode=0: This node don't do anything.
# mode=1: This node send the robot the position of target.
# mode=2: The robot is moving to the target.
#          This node subscribe the odom and check weather the robot is reaching the target.
mode_ = 0
robot=Robot()

def random_move_switch(req):
    """
    This is callback function of the server of service "/move_random"
    change the mode to 1 in order to send the robot the new target position.

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

def send_target_pos():
    """
    This is function to send the robot the position of the robot.
    
    When the client(rospy.ServiceProxy('/select_target', RandomPosition)) is trying to get the new target position,
    this data is saved as the instance value of robot (instance).
    Change the mode to 2.

    Parameters:
        ----------
        None

        Returns:
        ----------
        None
    """

    global mode_
    print('state1 : move randomly')
    set_target = rospy.ServiceProxy('/select_target', RandomPosition)
    response=set_target()
    robot.x_des=response.x
    robot.y_des=response.y
    robot.send_destination()
    mode_=2

def main():
    """
    This is main function and decide the robot motion depending on the mode of the robot.

    mode=0: This node don't do anything.
    mode=1: This node send the robot the position of target.
    mode=2: The robot is moving to the target.
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

    rospy.init_node('state1')
    
    reach_goal_srv = rospy.ServiceProxy("/reach_goal",SetBool)

    srv = rospy.Service('/move_random', SetBool,random_move_switch)
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        if mode_==0:
            rate.sleep()
            continue
        elif mode_==1:
            send_target_pos()
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