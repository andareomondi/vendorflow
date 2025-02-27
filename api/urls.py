from django.urls import path
from .views import *

urlpatterns = [
    path('', getRoutes, name="routes"),
    path('machines/', getMachines, name="machines"),
    path('machines/<str:pk>/', getMachine, name="machine"),
]
