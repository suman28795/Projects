from flask import Flask, request, render_template
import RPi.GPIO as GPIO
import time	

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

TRIG = 16
ECHO = 18
GPIO.setup(8, GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!!!"

@app.route("/water_level")
def water_level():
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
	level = 30 - distance
	if level <= 5:
		message = 'MOTOR ON'
		while level <= 20:
			GPIO.output(8, True)
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
			level = 30 - distance
		message = 'MOTOR ON'
		GPIO.output(8, True)
	elif level > 5:
		message = 'MOTOR OFF'
		GPIO.output(8, False)	
	else:
		message = 'MOTOR OFF'
		GPIO.output(8, False)
		GPIO.output(13, False)
        	GPIO.output(15, False)

	return render_template('lab_dist.html', message = message, level = level)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

