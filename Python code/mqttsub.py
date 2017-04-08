#required libraries
import sys                                 
import ssl
import json
import mosquitto as mqtt

# for motion sensor
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
#from datetime import datetime

#called while client tries to establish connection with the server 
def on_connect(mqttc, obj, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
        mqttc.subscribe("smartcam" , qos=0)

    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")
        

#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#called when a message is received by a topic

def on_message(mqttc, obj, msg):
    print("Received message from topic: "+msg.topic)
    timestamp = datetime.now()
    f = open("/home/pi/output/intruder_" + str(timestamp) + ".jpg", 'w')
    f.write(msg.payload)
    f.close()
#    data = str(msg.payload)

#    GPIO.setmode(GPIO.BCM)
#    GPIO.setwarnings(False)
#    GPIO.setup(16,GPIO.OUT)

#    if data == "HIGH":
#        GPIO.output(16,GPIO.HIGH)
#    else:
#        GPIO.output(16,GPIO.LOW)

#creating a client with client-id=mqtt-test
mqttc = mqtt.Mosquitto()

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 support as required by aws-iot service
mqttc.tls_set(ca_certs="/etc/mosquitto/certs/ca.crt",
	          certfile="/etc/mosquitto/certs/server.crt",
	          keyfile="/etc/mosquitto/certs/server.key",
              tls_version=ssl.PROTOCOL_TLSv1_2, 
              ciphers=None)
mqttc.username_pw_set("test", "rasp")

#connecting to aws-account-specific-iot-endpoint
mqttc.connect("192.168.43.89",8883)


mqttc.loop_forever()


    
