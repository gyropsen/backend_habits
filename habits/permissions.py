from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Класс для проверки на владение привычками
    """

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.owner == request.user
