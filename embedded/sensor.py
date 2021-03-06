#!/usr/bin/python

import Adafruit_DHT
import paho.mqtt.client as mqtt
import json, urlparse, time

# Sensor should be set to Adafruit_DHT.DHT11
sensor = Adafruit_DHT.DHT11
sensor_id = 1

# Example using a Raspberry Pi with DHT sensor
# connected to GPIO23.
sensor_pin = 23

# MQTT client setup
mqttClient = mqtt.Client()
# e.g. mqtt://username:password@m20.cloudmqtt.com:port
mqttConnectionString = ""
url = urlparse.urlparse(mqttConnectionString)
mqttClient.username_pw_set(url.username, url.password)
mqttClient.connect(url.hostname, port=url.port, keepalive=60, bind_address="")

# Loop to read data from sensor every 30 secondes
while True:
	# Try to grab a sensor reading.  Use the read_retry method which will retry up
	# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
	if humidity is not None and temperature is not None:
		temp_fmt = round(temperature, 1)
		hum_fmt = round(humidity, 1)
		print 'Temp=%s*C  Humidity=%s%%' % (temp_fmt, hum_fmt)

		# publish data to broker
		data = json.dumps({"sensor_id": sensor_id, "temperature": temp_fmt, "humidity": hum_fmt})
		if mqttClient.publish("rasp_sensor", data):
			print "Data published to broker: " + str(data)
		else:
			print "Failed to publish data to broker"
	else:
		print 'Failed to get reading. Try again!'

	time.sleep(30)

