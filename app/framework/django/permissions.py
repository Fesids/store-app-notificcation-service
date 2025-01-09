from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user["guid"] )

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        #return True
        return request.user and "admin" in request.user.roles
