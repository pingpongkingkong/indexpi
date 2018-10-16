import RPi.GPIO as GPIO, time
import math

port = 36
directionPort = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(port, GPIO.OUT)
GPIO.setup(directionPort, GPIO.OUT)

speed = 700

p = GPIO.PWM(port, speed)
p.start(50)

class Stepper:
	
	def __init__(self, diameterInCM):
		self.revsPerSecond = 3.21 # 0.65
		self.diameter = diameterInCM
		self.circ = math.pi * self.diameter
		self.p = GPIO.PWM(port, speed)
		print "Initialized: circumfrence is %f" % self.circ

	def goSpoolDistance(self, distance, direction):

		print "Calculating revs to go %f" % distance
		travelled = 0
		revs = 0
		currentDiameter = self.diameter
		while travelled < distance:
			travelled += math.pi * currentDiameter
			currentDiameter += 1
			revs += 1

		print "Would take %f" % revs

		secs = revs / self.revsPerSecond

		self.goTime(secs, direction)

	def goDistance(self, distance, direction):
		mmPerSec = self.circ * self.revsPerSecond
		waitTime = distance / mmPerSec
		print "Turning %f mm" % distance
		self.goTime(waitTime, direction)

	def goTime(self, waitTime, direction):
		GPIO.output(directionPort, direction)
		self.p.start(50)
		#print "Sleeping %f secs" % waitTime
		time.sleep( waitTime )
		self.p.stop()

	def __del__(self):
		print "In destructor"
		self.p.stop()
		GPIO.cleanup()
			

# The first movement is a complete revolution (@9V), the remainder are not, and they sound choppy.
def experiment_1(s):
	for i in range(0, 20):
		s.goDistance(15.707963 * 1, 1)
		time.sleep(0.3)
		s.goDistance(15.707963 * 1, 0)
		time.sleep(0.3)

	#s.goDistance(6.0 * 100)
	#s.goSpoolDistance(10000 )

s = Stepper(5)
try:
	experiment_1(s)
	#s.goDistance(15.707963 * 1, 0)
except:
	del s	
