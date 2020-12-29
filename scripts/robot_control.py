#! /usr/bin/env python

# import ros stuff
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
    elif state == 4:
        print('state4 :stop in the last position')
    else:
        rospy.logerr('Unknown state!')

def next_action(req):
    global updated_state_
    print('go to next action')
    updated_state_=False
    res = SetBoolResponse()
    res.success = True
    res.message = 'Done!'
    return res

def main():
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