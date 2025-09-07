from rest_framework import permissions

class IsCompanyAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff and request.user.details.get('is_manager', False))
    
class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser) 
    
class IsGetForAll(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.method == 'GET')