from django.conf import settings
from rest_framework import permissions

class IsDemandCloud(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth and request.auth.get('cloud') == 'demand' and settings.CLOUD_TYPE == 'demand'

class IsSupplyCloud(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth and request.auth.get('cloud') == 'supply' and settings.CLOUD_TYPE == 'supply'

