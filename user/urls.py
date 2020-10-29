"""classh User URL Configuration
author: Sanidhya Mangal
github: sanidhyamangal
"""
from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'user', views.UserViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls)),
]
