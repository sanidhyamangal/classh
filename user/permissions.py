"""
author: Sanidhya Mangal
github: sanidhyamangal
"""
from rest_framework.permissions import BasePermission


class AllowAnyPostReadUpdateDestroyOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user.uid == obj.user.uid
                or (request.user.is_superuser or request.user.is_staff))


class IsAuthenticatedOrOwnerOrAdmin(AllowAnyPostReadUpdateDestroyOwnerOrAdmin):
    def has_permission(self, request, view):
        return request.user.is_authenticated
