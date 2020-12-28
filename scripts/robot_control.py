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
des_pub = rospy.Publisher('/move_base/goal',MoveBaseActionGoal, queue_size=10)



def clbk_odom(msg):
    # position
    robot.x = msg.pose.pose.position.x
    robot.y = msg.pose.pose.position.y

    # yaw
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    robot.yaw = euler[2]

def judge_goal():
    global updated_state_
    err_pos = math.sqrt((robot.y_des - robot.y)**2 +(robot.x_des - robot.x)**2)
    print('err_pos='+str(err_pos))
    if(err_pos < 1.0):
        print('reach goal!!!!!')
        print('des_x='+str(robot.x_des))
        print('des_y='+str(robot.y_des))
        print('x='+str(robot.x))
        print('y='+str(robot.y))
        updated_state_=False


def send_destination():
    print('send the destination to the robot')
    move_base_action_goal=MoveBaseActionGoal()
    move_base_action_goal.goal.target_pose.header.frame_id="map"
    move_base_action_goal.goal.target_pose.pose.orientation.w=1
    move_base_action_goal.goal.target_pose.pose.position.x=robot.x_des
    move_base_action_goal.goal.target_pose.pose.position.y=robot.y_des
    print('des_x='+str(robot.x_des))
    print('des_y='+str(robot.y_des))
    des_pub.publish(move_base_action_goal)

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
        move_random()
    elif state == 2:
        user_input()
    elif state == 3:
        wall_follow_srv = rospy.ServiceProxy('wall_follower_switch',SetBool)
        response=wall_follow_srv(True)
    elif state == 4:
        print('state4')
    else:
        rospy.logerr('Unknown state!')

def main():
    global updated_state_
    rospy.init_node('robot_control')
    rate = rospy.Rate(20)
    updated_state_srv = rospy.ServiceProxy('/change_state',SetBool)
    sub_odom = rospy.Subscriber('/odom', Odometry, clbk_odom)
    while not rospy.is_shutdown():
        if not updated_state_:
            response=updated_state_srv()
            updated_state_=response.success
            state= rospy.get_param("state")
            change_action(state)
        else:
            judge_goal()
        rate.sleep()


if __name__ == '__main__':
    main()