"""
URL configuration for vendorflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from vending.views import *
from managment.views import *
from home.views import *
from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view(), name='home'),
    path('auth/register/', Register.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path("about/", About.as_view(), name="about"),
    path("machine/<int:pk>/", Specific_Machine.as_view(), name="specific_machine"),
    path("logout/", LogOut.as_view(), name="logout"),
    path("dashboard/", Dashboard.as_view(), name="dashboard"),
    path('user-overview-pdf/', user_overview_pdf, name='user_overview_pdf'),
    path("machine_pdf/<int:pk>/", machine_overview_pdf, name="specific_machine_pdf"),
    path("machine_register/", MachineRegistration.as_view(), name="register_machine"),
    path("machine/activation/<int:id>/", MachineActivation.as_view(), name="machine_activation"),
    path("machine/delete/<int:pk>", deleteMachine, name='delete_machine'),
    path("machine/update/<int:pk>", MachineUpdate.as_view(), name='machine_update'),
    path("refill/delete/<int:pk>", deleteRefill, name='delete_refill'),
    path("api/", include('api.urls')),
    path("shops/", Shops.as_view(), name="shops"),
    path("shops/<int:pk>/", SpecificShop.as_view(), name="specific_shop"),

    # path("api-auth/", include('rest_framework.urls', namespace='rest_framework')),
]

# Add static and media URLs
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)