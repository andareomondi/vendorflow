from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Transaction)
admin.site.register(Machine)
admin.site.register(Refill)
admin.site.register(Shop)