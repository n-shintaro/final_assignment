#! /usr/bin/env python

"""
    This is the file to change the state depending on user's command.
    If the robot is in state 1, or 2, the system should wait until the robot reaches the position.

        - state 1:
            move randomly in the environment, by choosing 1 out of 6 possible target positions:
            [(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)], implementing a random position service as in the assignment 1
        - state 2:
            directly ask the user of the next target position (checking that the position is one of the possible six)
        - state 3:
            start following the external walls
        - state 4:
            stop in the last position
"""

import rospy
import math
from robot import *
from std_srvs.srv import *
from std_msgs.msg import *
from final_assignment.srv import RandomPosition
from nav_msgs.msg import Odometry
from tf import transformations
from move_base_msgs.msg import MoveBaseActionGoal
# robot state variable

robot=Robot()
updated_state_=False

def change_state(state):
    """
        This is the function to change the state depending on user's command(state).
    
    - state 1:
        call the service as the client of '/move_random'.
    - state 2:
        call the service as the client of '/user_input'.
    - state 3:
        call the service as the client of 'wall_follower_switch'.
    - state 4:
        stop in the last position

    Parameters:
        ----------
        state:integer(1~4)
        This parameter decide the robot action.

        Returns:
        ----------
        None
    """
    if state == 1:
        print('state1 :move randomly in the environment')
        random_move_srv = rospy.ServiceProxy('/move_random',SetBool)
        response=random_move_srv(True)
    elif state == 2:
        print('state2 : ask the user of the next target position')
        user_input_srv = rospy.ServiceProxy('/user_input',SetBool)
        response=user_input_srv(True)
    elif state == 3:
        print('state3 : the robot follow the wall')
        wall_follow_srv = rospy.ServiceProxy('wall_follower_switch',SetBool)
        response=wall_follow_srv(True)
        updated_state_=False
    elif state == 4:
        print('state4 :stop in the last position')
        updated_state_=False
    else:
        rospy.logerr('Unknown state!')

def next_action(req):
    """
    This is callback function of the server of service "/reach_goal"

    This is called when the robot is reaching the position in the case that the robot's state is 1 or 2 and
    updated_state_ is changed to False in order to make one's next move.

    Parameters:
        ----------
        req :SetBool

        Returns:
        ----------
        res :SetBoolResponse
        return res.success = True  and res.message = 'Done!'

    """
    global updated_state_
    print('go to next action')
    updated_state_=False
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res

def main():
     """
        This is main function.

        If updated_state_=True, this node don't anything and
        just wait until the robot reaches the position.

        If updated_state_=False, this node try to change the robot state.
        call the service as the client of '/change_state'.

        Parameters:
        ----------
        None

        Returns:
        ----------
        None
    """
    global updated_state_
    rospy.init_node('robot_control')
    rate = rospy.Rate(10)
    s = rospy.Service('/reach_goal', SetBool, next_action)
    #reach_goal_s = rospy.Service('reach_goal', Empty, next_action)
    updated_state_srv = rospy.ServiceProxy('/change_state',SetBool)
    while not rospy.is_shutdown():
        if updated_state_:
            rate.sleep()
            #continue
        else:
            response=updated_state_srv()
            updated_state_=response.success
            state= rospy.get_param("state")
            change_state(state)
        rate.sleep()

if __name__ == '__main__':
    main()