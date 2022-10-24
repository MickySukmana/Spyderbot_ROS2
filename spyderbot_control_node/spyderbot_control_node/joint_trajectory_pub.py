#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration

from .submodule.inverse_kinematic import inverse_kinematic

from std_msgs.msg import String
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

class joint_trajectory_pub(Node):

	def __init__(self):
		super().__init__('joint_trajectory_pub')
		
		ik = inverse_kinematic(8, 6.8)
		drop = 5
		swing = 4

		self.fs = ik.calc(5, 6, swing)	
		self.fd = ik.calc(5, 6, drop)		
		self.rs = ik.calc(5, 4, swing)	
		self.rd = ik.calc(5, 4, drop)		
		self.ip = ik.calc(5, 5, drop)		
		self.ll = ik.calc(5, 7, drop)
		self.ips = ik.calc(5, 5, swing)
		self.str = ik.calc(5, 5, 0)

		topic = "/joint_trajectory_controller/joint_trajectory" 

		self.publisher_ = self.create_publisher(JointTrajectory, topic, 10)
		self.timer_period = 0.5
		self.timer = self.create_timer(self.timer_period, self.timer_callback)
		self.i = 0

	def timer_callback(self):
		timer = int(self.timer_period * 10**9)
		pos=[
			 self.ip + self.rd + self.ip + self.ip,
             self.ip + self.fs + self.ip + self.ip,
             self.ip + self.fd + self.ip + self.ip,
             self.fd + self.ip + self.fd + self.rd,
             self.fd + self.ip + self.rs + self.rd,
             self.fd + self.ip + self.rd + self.rd,
             self.fd + self.ip + self.rd + self.fs,
             self.fd + self.ip + self.rd + self.fd,
             self.ll + self.rd + self.ip + self.ip,
             self.ips + self.rd + self.ip + self.ip,
			]
		msg = JointTrajectory()

		msg.joint_names = ['rl1_joint', 'rl2_joint', 'rl3_joint',
						   'fl1_joint', 'fl2_joint', 'fl3_joint',
						   'rr1_joint', 'rr2_joint', 'rr3_joint',
						   'fr1_joint', 'fr2_joint', 'fr3_joint'
						  ]
		point = JointTrajectoryPoint()
		point.positions = pos[self.i]
		point.time_from_start = Duration(nanosec=timer) 
		
		msg.points.append(point)
		self.publisher_.publish(msg)
		self.i +=1
		if self.i >= 10:
			self.i = 0

def main(args=None):
	rclpy.init(args=args)
	
	joint_trajectory = joint_trajectory_pub()

	rclpy.spin(joint_trajectory)

	joint_trajectory.destroy_node()
	rclpy.shutdown()

if __name__ == '__main__':
	main()
