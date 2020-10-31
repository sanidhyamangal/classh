"""classh User URL Configuration
author: Sanidhya Mangal
github: sanidhyamangal
"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()

router.register(r'user', views.UserViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls)),
]
