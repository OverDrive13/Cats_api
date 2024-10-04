from rest_framework import permissions


class IsAdminModeratorAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Доступ к изменению объекта для админа, модератора и автора."""

    def has_object_permission(self, request, view, obj):
        """Выполнение запроса на конкретном объекте."""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)
