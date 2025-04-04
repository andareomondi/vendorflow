from .models import Machine

def sidebar_objects(request):
  if request.user.is_authenticated:
    machines = Machine.objects.filter(owner=request.user, activated=True)
    return {'sidebar_objects': machines}
  return {'sidebar_objects': []}
