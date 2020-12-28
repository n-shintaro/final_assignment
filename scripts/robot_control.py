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






def move_random():
    print('state1 : move randomly')
    set_target = rospy.ServiceProxy('/select_target', RandomPosition)
    response=set_target()
    robot.x_des=response.x
    robot.y_des=response.y
    send_destination()

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
        send_destination()
    else:
        print("value is invalid.\n You should choose from"+str(candidate_des_pos))
        return user_input()

def change_action(state):
    if state == 1:
        random_move_srv = rospy.ServiceProxy('/move_random',SetBool)
        response=random_move_srv(True)
    elif state == 2:
        user_input()
    elif state == 3:
        wall_follow_srv = rospy.ServiceProxy('wall_follower_switch',SetBool)
        response=wall_follow_srv(True)
    elif state == 4:
        print('state4')
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
            change_action(state)
        rate.sleep()

if __name__ == '__main__':
    main()