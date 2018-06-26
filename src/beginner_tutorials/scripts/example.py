#!/usr/bin/env python

# Software License Agreement (BSD License)
#
#  Copyright (c) 2018, Benjamin Narin
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution.
#   * Neither the name of the OSU Personal Robotics Group. nor the names of its
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#
# Author: Benjamin Narin

import roslib
roslib.load_manifest('beginner_tutorials')
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class stopper:
	def __init__(self):
		# Laser Scan To Subscribe to
		self.scan_sub = rospy.Subscriber('/scan',LaserScan,self.scan_callback)
		#self.move_sub = rospy.Subscriber('cmd_vel_mux/input/navi', Twist, self.move_callback)
		self.move_pub = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size = 10)
#		self.move_forward()
	#
	# def move_forward(self):
	# 	print "got here"
	# 	forward = Twist()
	# 	forward.linear.x = 1.0
	# 	self.move_pub.publish(forward)
	#
	#

	def scan_callback(self,scan): # combine move forward into this
		# Publish image
		# self.pub.publish(img)
		#print scan.ranges
		forward = Twist()
		forward.linear.x = 1.0
		is_near_wall = False
		for i in scan.ranges:
			if i <= 0.5:
				#print True
				#print "got to 66"
				self.move_pub.publish(Twist())
				is_near_wall = True
			if not is_near_wall:
				self.move_pub.publish(forward)


	def move_callback(self, twist):
		print "hey"



if __name__=='__main__':
	rospy.init_node('stopper')
	stopper = stopper()
	rospy.spin()
