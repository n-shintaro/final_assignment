#! /usr/bin/env python

# import ros stuff
import rospy
from std_srvs.srv import *
from std_msgs.msg import *
from final_assignment.srv import RandomPosition
from move_base_msgs.msg import MoveBaseActionGoal

updating_state_=False

def move_random():
    print('state1 : move randomly')
    set_target = rospy.ServiceProxy('/select_target', RandomPosition)
    response=set_target()
    des_pos_x=rospy.get_param('des_pos_x')
    des_pos_y=rospy.get_param('des_pos_y')
    
    des_pos_x=response.x
    des_pos_y=response.y
    # goal=MoveBaseActionGoal()
    # goal.target_pose.frame_id="map"
    # goal.target_pose.pose.orientation.w=1
    # goal.target_pose.pose.position.x=rospy.get_param('des_pos_x')
    # goal.target_pose.pose.position.x=rospy.get_param('des_pos_y')
    # des_pub(goal)



def main():
    global updating_state_
    rospy.init_node('robot_control')
    rate = rospy.Rate(20)
    des_pub = rospy.Publisher('/move_base/goal',MoveBaseActionGoal, queue_size=1)
    updated_state_srv = rospy.ServiceProxy('/change_state',SetBool)
    while not rospy.is_shutdown():
        state= rospy.get_param("state")
        if not updating_state_:
            response=updated_state_srv()
            updating_state_=response.success
        else:
            if state == 1:
                move_random()
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