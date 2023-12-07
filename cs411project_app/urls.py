"""
URL configuration for cs411project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import get_roadtrip_APIView, get_google_apikey

urlpatterns = [
    path("admin/", admin.site.urls),
    path('get_roadtrip/', get_roadtrip_APIView.as_view(), name='get_roadtrip'),
    path('get_google_apikey/', get_google_apikey.as_view(), name='get_google_apikey')
]
