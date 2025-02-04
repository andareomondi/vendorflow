from django.apps import AppConfig
import threading
from .mqtt_client import start_mqtt_client
class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'


    def ready(self):
        mqtt_thread = threading.Thread(target=start_mqtt_client)
        mqtt_thread.setDaemon(True)
        mqtt_thread.start()