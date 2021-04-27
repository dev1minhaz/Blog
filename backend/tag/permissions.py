from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsOwnerOrStaffUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user


def is_object_owned_by_user(target_obj_user_id, user_email):
    logged_in_user = get_user_model().objects.filter(email=user_email)[0]
    return str(target_obj_user_id) == str(logged_in_user.id)


class UserCanCreateOwnObject(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if not request.user.is_authenticated:
                return False
            if request.user.is_staff:
                return True
            if isinstance(request.data, list):
                results = [is_object_owned_by_user(target_obj.get(
                    'user'), request.user) for target_obj in request.data]
                return all(results)
            else:
                return is_object_owned_by_user(request.data.get('user'), request.user)
        return True