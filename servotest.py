# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.
 
import board
import busio
import adafruit_pca9685
import time
 
# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685
 
# Create the I2C bus interface.
i2c_bus = busio.I2C(board.SCL, board.SDA)
 
# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)
 
# Set the PWM frequency to 60hz.
pca.frequency = 50

microsecond_value = 3.3983

#set the pwm output signal AKA duty cycle
pca.channels[0].duty_cycle = int( microsecond_value * 1500) # 1 ms


#now lets go from the min to max value back and forth
incrementing = True
pwm_max = 2200
pwm_min = 800
pwm_current = 1000
pwm_step = 50

while True:

	if incrementing:
		pwm_current = pwm_current + pwm_step
		if pwm_current >= pwm_max:
			incrementing = False
			time.sleep(.25)
	else:
		pwm_current = pwm_current - pwm_step
		if pwm_current <= pwm_min:
			incrementing = True
			time.sleep(.25)

	pca.channels[0].duty_cycle = int( microsecond_value * pwm_current)
	pca.channels[8].duty_cycle = int( microsecond_value * pwm_current)
		
	time.sleep(.025)