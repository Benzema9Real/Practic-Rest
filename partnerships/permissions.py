from rest_framework import permissions

class IsSupplier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Supplier').exists()

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user



class IsBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Buyer').exists()
