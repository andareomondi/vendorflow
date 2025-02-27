from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import *
# Create your views here.
@api_view(['GET'])
def getRoutes(request):
  routes = [
      {
          'Endpoint': '/machines/',
          'method': 'GET',
          'body': None,
          'description': 'Returns an array of machines'
      },
      {
          'Endpoint': '/machines/id',
          'method': 'GET',
          'body': None,
          'description': 'Returns a single note object'
      },
  ]
  return Response(routes)

@api_view(['GET'])
def getMachines(request):
    machines = Machine.objects.all()
    serializer = MachineSerializer(machines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getMachine(request, pk):
    machine = Machine.objects.get(id=pk)
    serializer = MachineSerializer(machine, many=False)
    return Response(serializer.data)