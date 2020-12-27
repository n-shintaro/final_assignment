#! /usr/bin/env python

# import ros stuff
import rospy
from std_srvs.srv import *

# service callback
def isInteger(n):
    """Return True if argument is a whole number, False if argument has a fractional part.

    Note that for values very close to an integer, this test breaks. During
    superficial testing the closest value to zero that evaluated correctly
    was 9.88131291682e-324. When dividing this number by 10, Python 2.7.1 evaluated
    the result to zero"""

    if n%2 == 0 or (n+1)%2 == 0:
        return True
    return False

def get_new_state(req):
    print("Please insert a new state from 1 to 4")
    try:
        state = float(raw_input('state :'))
    except:
        print("an error occurred")
        return get_new_state(req)
    if state<=5 and state>=1 and isInteger(state):
        print("Thanks! Let's change the state")

        rospy.set_param("state", state)
    else:
        print("please enter 1, 2, 3 and 4")
        return get_new_state(req)
    return []


def main():
    rospy.init_node('decide_state')
    state= rospy.get_param("state")
    print("Hi! We are finishing the state: state = " +
          str(state))
    srv = rospy.Service('/change_state', Empty, get_new_state)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == '__main__':
    main()
