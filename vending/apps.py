import threading
import time
from django.apps import AppConfig
from .mqtt_client import start_mqtt_client

class VendingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vending'
    mqtt_thread = None
    tokenization_thread = None

    def ready(self):
        if not VendingConfig.mqtt_thread or not VendingConfig.mqtt_thread.is_alive():
            # Start the MQTT client in a separate thread
            VendingConfig.mqtt_thread = threading.Thread(target=start_mqtt_client)
            VendingConfig.mqtt_thread.setDaemon(True)
            VendingConfig.mqtt_thread.start()

        if not VendingConfig.tokenization_thread or not VendingConfig.tokenization_thread.is_alive():
            # Start the daily tokenization task in a separate thread
            VendingConfig.tokenization_thread = threading.Thread(target=self.run_daily_tokenization)
            VendingConfig.tokenization_thread.setDaemon(True)
            VendingConfig.tokenization_thread.start()

    def run_daily_tokenization(self):
        while True:
            self.process_daily_tokenization()
            time.sleep(86400)  # Sleep for one day (86400 seconds)

    def process_daily_tokenization(self):
        from .models import Machine
        from datetime import datetime
        # filter only activated machines
        machines = Machine.objects.filter(activated=True)
        current_date = datetime.now().date()
        for machine in machines:
            machine.process_daily_usage()
