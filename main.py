# damei@dameiSolutions


import socket
import threading 
import time
import helper

BROADCAST_PORT = 6000
STATUS_PORT = 6001
CALL_PORT = 6002
SELF_P_NUM = '9660570748'
MAX = 40000
MAX_DGRAM = 40000
DEVICE_HANDLER_PORT = 6003
THREAD_CONTROLLER = 4

class nodeHandler:
	## class initializer ##
	def __init__(self,phoneNum) :
		self.connectedDevices = []
		self.pft = {}
		self.deviceHandler()
		self.isFree = True
		thread = threading.Thread( target = self.callReciever , args = ())
		thread.start()
		thread = threading.Thread( target = self.statusInformer , args = ())
		thread.start()

	##
	##	deviceHandler  -->  The android device when connected to hotspot keeps on notifying discovery server after regular intervals of time
	##
	def deviceHandler(self) :
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind(('',DEVICE_HANDLER_PORT))
		while True :
			data , address = s.recvfrom(MAX_DGRAM)
			if data[:4] == 'CALL' :
				thread = threading.Thread(target = self.makeCall , args = ( int(data[4:]),address[0] , address[1] ))
				thread.start()

	def makeCall(self) :
		location = self.locate()

	def locate(self,phoneNum) :
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.bind(('',BROADCAST_PORT))
		s.settimeout(3)
		helper.broadcast('192.168.',THREAD_CONTROLLER,phoneNum,BROADCAST_PORT)
		try :
			data , address = s.recvfrom(MAX)
			if data == self.phoneNumber :
				location = address[0]
			else :
				location = 'NULL'
		except socket.error as error :
			location = 'NULL'
		return location

	## statusInformer 
	## Every incoming call
	def statusInformer(self) :
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind(('',STATUS_PORT))
		data , address = s.recvfrom(MAX)
		if self.isFree :
			s.sendto('FREE',(address))
		else :
			s.sendto('BUSY',(address))
	##
	##	callReciever
	##	The server side of the incoming call	
	def callReciever(self) :
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind(('',CALL_PORT))
		s.listen(1)
		c , address = s.accept()
		c.send("HELLO")
		# To be continued
	###


	def checkRemoteStatus(self,location) :
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.sendto('STATUS',(location,STATUS_PORT))
		data , address = s.recvfrom(MAX)
		if data == 'FREE' :
			return True
		else :
			return False

	def call(self,phoneNum) :
		location = self.locate(phoneNum)
		if location == 'NULL' :
			print  'Number not found'
		else :
			if self.checkRemoteStatus(location) :
				self.isFree = False
				print 'Connecting...'
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
				s.connect((location,CALL_PORT))
				s.recv(MAX)
				temp = raw_input()
				self.isFree = True
			else :
				print 'Number Busy'



dialer = app(SELF_P_NUM)
dialer.call('9660570748')


