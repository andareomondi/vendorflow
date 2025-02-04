import json
import paho.mqtt.client as mqtt
broker_address = "localhost"
broker_port = 1883
username = 'test'
password = 'test'
topic = 'PLC_VENDING'



def on_message(client, userdata, msg):
    msg = msg.payload.decode('utf-8')
    print(msg)



def on_connnect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)
    else:
        print(f"Failed to connect with result code {rc}")

# creating an instance of the mqtt client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.username_pw_set(username, password)
client.on_connect = on_connnect

def start_mqtt_client():
    try:
        client.connect(broker_address, broker_port, 60)
        client.loop_start()
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        client.loop_stop()