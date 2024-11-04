#!/usr/bin/env python3

import rospy
import yaml
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

def load_waypoints(file_path):
    with open(file_path, 'r') as file:
        waypoints = yaml.safe_load(file)
    return waypoints['waypoints']

def send_goal(x, y, frame_id="map"):
    # MoveBaseAction 클라이언트 생성
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    
    # 서버 연결 대기
    rospy.loginfo("Waiting for move_base action server...")
    client.wait_for_server()
    rospy.loginfo("Connected to move_base server")

    # 목표 설정
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = frame_id
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0  # 방향 설정 (여기서는 기본 방향)

    # 목표 전송
    rospy.loginfo("Sending goal: x={}, y={}".format(x, y))
    client.send_goal(goal)

    # 결과 대기
    client.wait_for_result()
    
    if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("도착 완료: 목표 지점 x={}, y={}".format(x, y))
    else:
        rospy.loginfo("목표에 도달하지 못했습니다.")

def main():
    rospy.init_node('waypoint_navigation')

    # YAML 파일에서 waypoint 로드
    waypoints = load_waypoints('/home/hunter/catkin_ws/src/Agilex/hunter_ros/husky_gps_nav/config/waypoints.yaml')

    
    for waypoint in waypoints:
        x = waypoint['x']
        y = waypoint['y']
        send_goal(x, y)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
