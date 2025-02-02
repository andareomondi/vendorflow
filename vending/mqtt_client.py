import paho.mqtt.client as mqtt
broker_address = "102.130.118.195"
broker_port = 1883
username = 'test'
password = 'test'
topic = 'PLC_VENDING'


# function to handle messages being posted
def on_message(client, userdata, msg):
    from .models import Machine, Transaction    
    msg = msg.payload.decode('utf-8')
    print(msg)
    if not msg == '':
        try:
            serial = msg['serial_no']
            amount = msg['amount']
            volume = msg['volume']
            total_amount = msg['total_amount']
            total_volume = msg['total_volume']
            machine = Machine.objects.get(serial_number = serial)
            if machine.exists() and machine.remaining_tokens > 1:
                transaction = Transaction(machine = machine, amount = amount, volume = volume, total_amount = total_amount, total_volume = total_volume)
                transaction.save()
                transaction.remaining_tokens()
        except Exception as e:
            print(e)
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