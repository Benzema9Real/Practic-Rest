from rest_framework import permissions


from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class Editor(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверка, аутентифицирован ли пользователь
        if not request.user.is_authenticated:
            raise PermissionDenied("Доступ запрещён: пользователь не аутентифицирован.")

        # Проверка, существует ли профиль пользователя
        if not hasattr(request.user, 'avatar'):
            raise PermissionDenied("Доступ запрещён: у пользователя нет профиля.")

        # Проверка роли пользователя
        if request.user.avatar.role != 'editor':
            raise PermissionDenied("Доступ запрещён: необходимы права редактора.")

        return True