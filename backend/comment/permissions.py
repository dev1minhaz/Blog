from rest_framework import permissions


class OwnerCanUpdateOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH"]:
            return obj.user == request.user
        if request.method == "DELETE":
            if request.user.is_staff:
                return True
            return obj.user == request.user
        return True
