#!/usr/bin/env python

"""
This is the file to generate tha random target position from [(-4,-3),(-4,2),(-4,7),(5,-7),(5,-3),(5,1)]
This node response and send the the random target position as the client of '/select_target'.
"""
import rospy
from std_msgs.msg import String
from final_assignment.srv import RandomPosition
from final_assignment.srv import RandomPositionResponse
import random

def generate_random(req):
    """
        generate tha random target position from [(-4,-3),(-4,2),(-4,7),(5,-7),(5,-3),(5,1)]

        Parameters:
        ----------
        req: RandomPosition

        Returns:
        ----------
        pos_x: float
        pos_y: float
        The new target position
    """

    index=random.randint(0,5)
    candidate_des_pos=[(-4,-3),(-4,2),(-4,7),(5,-7),(5,-3),(5,1)]
    pos_x=candidate_des_pos[index][0]
    pos_y=candidate_des_pos[index][1]
    print('pos_x='+str(pos_x))
    print('pos_y='+str(pos_y))
    return pos_x,pos_y

def add_target_server():
    """
        This is the function to declare the server of '/select_target'
        in order to send the new target position.

        Parameters:
        ----------
        None

        Returns:
        ----------
        None
    """

    server = rospy.Service('/select_target', RandomPosition, generate_random)
    print("Ready to add target position")
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node('target_server')
    add_target_server()
