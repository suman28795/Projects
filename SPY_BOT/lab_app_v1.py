import RPi.GPIO as GPIO
from flask import Flask, request, render_template                            
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


app = Flask(__name__)                                                        

TRIG = 16
ECHO = 18
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
pwm=GPIO.PWM(8,50)
pwm.start(5)

@app.route("/")
def hello():
    return render_template('bot_specs.html')                                                    
@app.route("/bot_control/<state>")
def bot_control(state=None):                                                 
    if state == 'up':
	pwm.ChangeDutyCycle(5)
 	GPIO.output(26, True)
	GPIO.output(19, True)                                                        	GPIO.output(21, True)
	GPIO.output(23, False)
	GPIO.output(24, True)
	GPIO.output(22, False)
        state ='up'
    if state == 'down':
	GPIO.output(26, True)
	GPIO.output(19, True)                                                        	GPIO.output(21, False)
	GPIO.output(23, True)
	GPIO.output(24, False)
	GPIO.output(22, True)
        state = 'down'
    if state == 'stop':
	pwm.ChangeDutyCycle(5)
	GPIO.output(26, True)
	GPIO.output(19, True)                                                        	GPIO.output(21, False)
	GPIO.output(23, False)
	GPIO.output(24, False)
	GPIO.output(22, False)
        state = 'stop'
    if state == 'left':
	pwm.ChangeDutyCycle(4.5)
	GPIO.output(26, True)
	GPIO.output(19, True)                                                        	GPIO.output(21, True)
	GPIO.output(23, False)
	GPIO.output(24, True)
	GPIO.output(22, False)
	state = 'left'
    if state == 'right':
	pwm.ChangeDutyCycle(5.5)
	GPIO.output(26, True)
	GPIO.output(19, True)                                                        	GPIO.output(21, True)
	GPIO.output(23, False)
	GPIO.output(24, True)
	GPIO.output(22, False)
	state = 'right'

    return render_template('bot1.html',title=state)

@app.route("/lab_temp")
def lab_temp():
	import sys
	import Adafruit_DHT
	humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 17)
 	if humidity is not None and temperature is not None:
		return render_template("lab_temp.html",temp=temperature,hum=humidity)
	else:
		return render_template("no_sensor.html")

@app.route("/lab_dist")
def Hcsr04():
    	GPIO.output(TRIG, False)
    	time.sleep(2)
    	GPIO.output(TRIG, True)
    	time.sleep(0.00001)
    	GPIO.output(TRIG, False)
    	while GPIO.input(ECHO)==0:
     	  pulse_start = time.time()
    	while GPIO.input(ECHO)==1:
    	  pulse_end = time.time()     
    	pulse_duration = pulse_end - pulse_start
    	distance = pulse_duration * 17150
    	distance = round(distance, 2)

	return render_template('lab_dist.html', dist=distance)

@app.route("/camera")
def camera():
	return render_template('camera.html')

if __name__ == "__main__":                                                   
    app.run(host='0.0.0.0', port=8080)
