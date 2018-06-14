# Import packages
import paho.mqtt.client as mqtt
import ssl
import time
from datetime import datetime
import rainbowhat as rh
import json

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 30

# Cloud Configuration (Host, Certification file, Private Key)
MQTT_HOST = 'ae5abd95v8i8t.iot.us-east-2.amazonaws.com'
CA_ROOT_CERT_FILE = 'root-CA.crt'
THING_CERT_FILE = 'device_virtual.cert.pem'
THING_PRIVATE_KEY = 'device_virtual.private.key'

# MQTT Toppic setting
MQTT_TOPIC1 = "sense/temp"
MQTT_TOPIC2 = "sense/pressure"

def timestamp():
    stamp  = str(datetime.now())
    return stamp[0:19]

def temp():
    temp = str(rh.weather.temperature())
    return temp[0:4]

def pressure():
    pressure = str(rh.weather.pressure())
    return pressure

# Define callback function for publishing
def on_publish(client, userdata, mid):
	print("A message published successfully!")

def on_connect(mosq, obj, flags, rc):
    print('connected')
	
# Initiate MQTT Client
mqttc = mqtt.Client()

# Register publish callback function
mqttc.on_publish = on_publish
mqttc.on_connect = on_connect

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)		
mqttc.loop_start()

# Send magnetometer and sensors information every second and 50 times
count = 0

while (count < 50):

    # Sensors Message Form
    msg_t = {'Temperature' : temp(), 'Timestamp': timestamp() }
    msg_p = {'Pressure' : pressure(), 'Timestamp': timestamp() }
    MQTT_Temp = json.dumps(msg_t)
    MQTT_Press = json.dumps(msg_p)

    # Publish Sensor info
    mqttc.publish(MQTT_TOPIC1,MQTT_Temp,qos=1)
    mqttc.publish(MQTT_TOPIC2,MQTT_Press,qos=1)
    
    time.sleep(10)
    count += 1
    
# Disconnect from MQTT_Broker
mqttc.disconnect()
