#!/usr/bin/python3
# publisher

#required libraries for mqtt and AWS IoT
import sys
import ssl
import json
import mosquitto as mqtt

import smtplib
# for motion sensor
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
from picamera import PiCamera

#creating a client with client-id=mqtt-test
#mqttc = mqtt.Client(client_id="test")
mqttc = mqtt.Mosquitto()

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/etc/mosquitto/certs/ca.crt",
                    certfile="/etc/mosquitto/certs/server.crt",
                    keyfile="/etc/mosquitto/certs/server.key",
                tls_version=ssl.PROTOCOL_TLSv1_2,
                ciphers=None)
mqttc.username_pw_set("test", "rasp")


mqttc.connect("192.168.43.89",8883)


# start a new thread handling communication with AWS IoT
mqttc.loop_start()

try:
    sensor = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)

    curr = False
    i = 0
    j = 0	
    USER = 'atnsproj@gmail.com'
    PASS = 'teamproj'	
    while i < 10:
	curr = GPIO.input(sensor)
    	camera = PiCamera()
      	if curr != False:
    		print "Motion Detected"
		if i == 0:
			server = smtplib.SMTP('smtp.gmail.com',587)
			server.ehlo()
			server.starttls()
			server.login(USER,PASS)
			
			msg = "Intruder Detected!"
			server.sendmail(USER, "blpavan007@gmail.com",msg)
			server.quit()
		i = i + 1
		timestamp = datetime.now()
		camera.capture("/home/pi/input/intruder_" + str(timestamp) + ".jpg")
		time.sleep(5)
		camera.close()
		f = open("/home/pi/input/intruder_" + str(timestamp) + ".jpg", "rb")
		payload = f.read()
    		msg_info = mqttc.publish("smartcam", payload, qos=1)
        else:
		print "No Motion Detected"
                camera.close()
	

except KeyboardInterrupt:
    pass

GPIO.cleanup()


