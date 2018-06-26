#!/usr/bin/env python



import roslib
roslib.load_manifest('beginner_tutorials')
import rospy
from std_msgs.msg import Header
from geometry_msgs.msg import Twist, TwistStamped
from sensor_msgs.msg import LaserScan
from message_filters import TimeSynchronizer, Subscriber
import time



class teleop_and_stop:
	def __init__(self):
		#self.move_sub = Subscriber()
		self.scan_sub = Subscriber('/scan',LaserScan)
		#self.scan_sub.registerCallback(self.test_scan_callback)
		self.move_pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size = 10)
		self.teleop_sub = rospy.Subscriber('/my_teleop', Twist, self.add_stamp)
		self.altered_input_pub = rospy.Publisher('/my_altered_input', TwistStamped, queue_size = 10)
		self.altered_input_sub = Subscriber('/my_altered_input', TwistStamped)
		#self.altered_input_sub.registerCallback(self.altered_input_callback)
		self.ats = TimeSynchronizer([self.altered_input_sub, self.scan_sub], queue_size=10)
		self.ats.registerCallback(self.scan_callback)

	def add_stamp(self, input):
		output = TwistStamped()
		output.twist = input
		output.header = Header()
		output.header.stamp = rospy.Time.now()
		self.altered_input_pub.publish(output)
		#prin/cmd_vel_mux/input/teleopt "at line 33"

	def altered_input_callback(self, input):
		print "got altered input"

	def test_scan_callback(self, scan):
		print "got a scan"



	def scan_callback(self,vel,scan): #For some reason it never gets here!
		near_wall = False
		for i in scan.ranges:
			if i <= 0.5 and vel.twist.linear.x >= 0:
				#print True
				self.move_pub.publish(Twist())
				near_wall = True
			elif (not near_wall):
				self.move_pub.publish(vel.twist)




if __name__=='__main__':
	rospy.init_node('teleop_and_stop')
	teleop = teleop_and_stop()
	rospy.spin()
