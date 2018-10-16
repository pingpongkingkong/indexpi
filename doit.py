import RPi.GPIO as GPIO, time
import math

port = 36
directionPort = 32
GPIO.setmode(GPIO.BOARD)
GPIO.setup(port, GPIO.OUT)
GPIO.setup(directionPort, GPIO.OUT)

direction = 0
speed = 600

p = GPIO.PWM(port, speed)
p.start(50)

try:
	while 1:
		print "Mach %i\n" % speed
		#time.sleep(1)
		direction = 1 - direction
		GPIO.output(directionPort, direction)
		time.sleep(14)
		#speed *= 1.1
		#p.ChangeFrequency(speed)
except:
	p.stop()
	GPIO.cleanup()
