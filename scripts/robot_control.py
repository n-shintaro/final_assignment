#! /usr/bin/env python

# import ros stuff
import rospy
from std_srvs.srv import *
from std_msgs.msg import *
from final_assignment.srv import RandomPosition
from move_base_msgs.msg import MoveBaseActionGoal

updating_state_=False
des_pub = rospy.Publisher('/move_base/goal',MoveBaseActionGoal, queue_size=1)
    

def send_destination():
    print('send the destination to the robot')
    move_base_action_goal=MoveBaseActionGoal()
    move_base_action_goal.goal.target_pose.header.frame_id="map"
    move_base_action_goal.goal.target_pose.pose.orientation.w=1
    move_base_action_goal.goal.target_pose.pose.position.x=rospy.get_param('des_pos_x')
    move_base_action_goal.goal.target_pose.pose.position.y=rospy.get_param('des_pos_y')
    des_pub.publish(move_base_action_goal)

def move_random():
    print('state1 : move randomly')
    set_target = rospy.ServiceProxy('/select_target', RandomPosition)
    response=set_target()
    des_pos_x=rospy.get_param('des_pos_x')
    des_pos_y=rospy.get_param('des_pos_y')
    des_pos_x=response.x
    des_pos_y=response.y
    send_destination()
def user_input():
    print('state1 : user input the destination')
    candidate_des_pos_x=[-4,-4,-4,5,5,5]
    candidate_des_pos_y=[-3,2,7,-7,-3,1]
    candidate_des_pos=[(-4,-3),(-4,2),(-4,7),(5,-7),(5,-3),(5,1)]
    print("Please insert a new state from "+str(candidate_des_pos))
    try:
        des_x = float(raw_input('state :'))
        des_y =float(raw_input('state :'))
    except:
        print("an error occurred")
        return user_input()
    if candidate_des_pos_x.index(des_x)==candidate_des_pos_y.index(des_y):
        print("Thanks! Let's change the des")
        des_pos_x=des_x
        des_pos_y=des_y
        send_destination()
    else:
        print("please enter from"+str(candidate_des_pos))
        return user_input()


def change_action(state):

    if state == 1:
        move_random()
    elif state == 2:
        user_input()
    elif state == 3:
        print('state3')
    elif state == 4:
        print('state4')
    else:
        rospy.logerr('Unknown state!')


def main():
    global updating_state_
    rospy.init_node('robot_control')
    rate = rospy.Rate(20)
    updated_state_srv = rospy.ServiceProxy('/change_state',SetBool)
    while not rospy.is_shutdown():
        if not updating_state_:
            response=updated_state_srv()
            updating_state_=response.success
            state= rospy.get_param("state")
            change_action(state)
            
        rate.sleep()


if __name__ == '__main__':
    main()