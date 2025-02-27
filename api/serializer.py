from rest_framework.serializers import ModelSerializer
from vending.models import Machine, Refill

class MachineSerializer(ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'
class RefillSerializer(ModelSerializer):
    class Meta:
        model = Refill
        fields = ['machine', 'payment_made',  'token_pack']