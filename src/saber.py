#!/usr/bin/env python3
#import arduinoserial
from pysabertooth import Sabertooth
from std_msgs.msg import String 
from geometry_msgs.msg import Twist, Pose
import rospy , time
import serial.tools.list_ports as port
#import pylcdlib
print ("\nInit sabertooth....\n")

print ("\nDetecting sabertooth....\n")
portlist = list(port.comports())
print (portlist)
address = ''
for p in portlist:
    print (p)
    if 'Sabertooth' in str(p):
        address = str(p).split(" ")
print ("\nAddress found @")
print (address[0])
speed1 = 0
speed2 = 0

saber = Sabertooth(address[0], baudrate=9600, address=128, timeout=0.1)
lower_limit = 10
upper_limit = 100

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def callback(data):
    speed = translate(data.linear.x,-1,1,-100,100)
    angle = translate(-data.angular.z,-1,1,100,-100)
    if angle+speed > 100:
        speed1 = 100
    else :
        speed1 = int(angle+ speed)
    
    if speed-angle < -100:
        speed2 = -100
    else :
        speed2 = int(speed-angle)
    
    if(abs(speed1) < lower_limit):
        speed1 = 0    
    if(abs(speed2) < lower_limit):
        speed2 = 0
    if(abs(speed1) > upper_limit):
        speed1 = upper_limit    
    if(abs(speed2) > upper_limit):
        speed2 = upper_limit


    if(data.linear.x == 0 and data.angular.z == 0):
        speed1 = 0
        speed2 = 0
        print("robot_stopped",speed1,speed2)

    if(angle < 0):
        print ("negative")
        saber.drive(1,speed2)
        saber.drive(2,speed1)
    elif (angle >= 0):
        print ("positive")
        saber.drive(1,speed2)
        saber.drive(2,speed1)
    

    

def sabertoothStatusCallback(data):
    print (data)
    temperature = ('T [C]: {}'.format(saber.textGet('m2:gett')))
    
    saber.textGet('T,start')
    set_position = ('P : {}'.format(saber.textGet('T,p45')))
    saber.textGet('1, home')
    
    battery = ('battery [mV]: {}'.format(saber.textGet('m2:getb'))) 
    print (battery , temperature)
    
    


    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/cmd_vel", Twist, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()



