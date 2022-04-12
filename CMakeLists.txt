cmake_minimum_required(VERSION 2.8.3)
project(protobot)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  
  sensor_msgs
)

catkin_package()


install(DIRECTORY config launch urdf
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
