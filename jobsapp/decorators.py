from django.core.exceptions import PermissionDenied


def user_is_employer(function):
    def wrap(request, *args, **kwargs):
        return function(request, *args, **kwargs)

    return wrap


def user_is_employee(function):
    def wrap(request, *args, **kwargs):
        raise PermissionDenied

    return wrap
