#! /usr/bin/env python

# import ros stuff
"""
    This is the file to ask user to decide the new state of the robot
    when the service "/change_state" is called.
    We make the user requested to choose from the state 1~4.

        -state 1:
            move randomly in the environment, by choosing 1 out of 6 possible target positions:
            [(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)], implementing a random position service as in the assignment 1
        - state 2:
            directly ask the user of the next target position (checking that the position is one of the possible six)
        - state 3:
            start following the external walls
        -state 4:
            stop in the last position
"""

import rospy
from std_srvs.srv import *


# service callback
def isInteger(number):
    """
    Return True if argument is integer, False if argument is not integer.

    Parameters:
        ----------
        number: float

        Returns:
        ----------
        Bool

    """

    if number%2 == 0 or (number+1)%2 == 0:
        return True
    return False

def get_new_state(req):
    """
    This is callback function of the server of service "/change_state"

    In order to the robot execute one of 4 behaviors,
    we make the user requested to choose from the state 1~4.
    When the previous state is 3, rhis commands the robot to stop following the wall.
    
    Parameters:
        ----------
        req :SetBool

        Returns:
        ----------
        res :SetBoolResponse
        When we can succeed in getting the state from 1 to 4,
        return res.success = True  and res.message = 'Done!'

    """

    print("Please insert a new state from 1 to 4")
    pre_state= rospy.get_param("state")

    print("Hi! update state from = " +
          str(pre_state))
    try:
        state = float(raw_input('state :'))
    except:
        print("an error occurred")
        return get_new_state(req)
    # check user input(state) is wether 1<=state<=4 and state is integer.
    if state<=4 and state>=1 and isInteger(state):
        print("Thanks! Let's change the state")
        rospy.set_param("state", state)
        res = SetBoolResponse()
        res.success = True
        res.message = 'Done!'
        if pre_state==3:
            # stop following the wall.
            wall_follow_stop_srv = rospy.ServiceProxy('wall_follower_switch',SetBool)
            response=wall_follow_stop_srv(False)
    else:
        print("please enter 1, 2, 3 and 4")
        return get_new_state(req)
    return res



def main():
    """
        initialize the node 'decide_state'.
        the server rospy.Service('/change_state',SetBool, get_new_state).
        is called.

        Parameters:
        ----------
        None

        Returns:
        ----------
        None
    """

    rospy.init_node('decide_state')
    srv = rospy.Service('/change_state',SetBool, get_new_state)
    rospy.spin()


if __name__ == '__main__':
    main()
