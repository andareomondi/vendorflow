from django.apps import AppConfig
import threading
from .mqtt_client import start_mqtt_client

class VendingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vending'

    def ready(self):
        # Start the MQTT client in a separate thread
        mqtt_thread = threading.Thread(target=start_mqtt_client)
        mqtt_thread.setDaemon(True)
        mqtt_thread.start()
