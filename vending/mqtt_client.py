import asyncio
import json
import paho.mqtt.client as mqtt
from django.db import IntegrityError

broker_address = "localhost"
broker_port = 1883
username = 'test'
password = 'test'
topic = 'PLC_VENDING'

async def process_message(data):
    from .models import Machine, Transaction
    try:
        serial = data['serial_no']
        amount = data['amount']
        volume = data['volume']
        total_amount = data['total_amount']
        total_volume = data['total_volume']

        machine = await asyncio.to_thread(Machine.objects.get, serial_number=serial)
        if machine and machine.remaining_tokens > 1:
            transaction = Transaction(
                machine=machine,
                amount=amount,
                volume=volume,
                total_amount=total_amount,
                total_volume=total_volume
            )
            await asyncio.to_thread(transaction.save)
            await asyncio.to_thread(machine.remaining_tokens)  # Assuming this updates the remaining tokens
    except json.JSONDecodeError:
        print("JSON decode error")
    except Machine.DoesNotExist:
        print(f"Machine with serial number {serial} does not exist.")
    except IntegrityError as e:
        print(f"Database integrity error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def on_message(client, userdata, msg):
    msg = msg.payload.decode('utf-8')
    print(f"Received message: {msg}")
    if msg:
        try:
            formatted_msg = msg.replace("'", '"')
            data = json.loads(formatted_msg)
            asyncio.run(process_message(data))
        except json.JSONDecodeError:
            print("JSON decode error")
        except Exception as e:
            print(f"Unexpected error: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)
    else:
        print(f"Failed to connect with result code {rc}")

client = mqtt.Client()
client.on_message = on_message
client.username_pw_set(username, password)
client.on_connect = on_connect

def start_mqtt_client():
    try:
        client.connect(broker_address, broker_port, 60)
        client.loop_start()
    except Exception as e:
        # print(f"Error connecting to MQTT broker: {e}")
        client.loop_stop()
