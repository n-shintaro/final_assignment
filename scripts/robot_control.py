#! /usr/bin/env python

# import ros stuff
import rospy
from std_srvs.srv import *
def main():

    rospy.init_node('robot_control')

    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        srv = rospy.ServiceProxy('/change_state',Empty)
        state = rospy.get_param('1')
        if not active_:
            continue
        else:
            state= rospy.get_param("state")
            if state == 1:
                print('state1')
            elif state == 2:
                print('state2')
            elif state == 3:
                print('state3')
            elif state == 4:
                print('state4')
            else:
                rospy.logerr('Unknown state!')
        rate.sleep()


if __name__ == '__main__':
    main()