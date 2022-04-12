from pysabertooth import Sabertooth

saber = Sabertooth('/dev/ttyACM0', baudrate=115200, address=128, timeout=0.1)

# drive(number, speed)
# number: 1-2
# speed: -100 - 100
count = 1
speed = 30
while(count<10000):
	saber.drive(1, speed)
	saber.drive(2, speed)
	
saber.stop()
