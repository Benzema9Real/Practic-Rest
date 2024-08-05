from rest_framework import permissions

class IsCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Company').exists()

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



class IsPerson(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Person').exists()
