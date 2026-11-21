from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'student')

class IsFaculty(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'faculty' or request.user.is_superuser))

class IsFacilityManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'facility_manager' or request.user.is_superuser))

class IsTechnician(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'technician' or request.user.is_superuser))

class IsDepartmentApprover(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'department_approver' or request.user.is_superuser))

class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.role == 'administrator' or request.user.is_superuser))

class CanBookFacility(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in ['student', 'faculty', 'facility_manager', 'administrator']

class CanApprove(permissions.BasePermission):
    """Restricted actions require Department Approver or Administrator role."""
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in ['department_approver', 'administrator'] or request.user.is_superuser

class CanManageMaintenance(permissions.BasePermission):
    """Triage and technician assignments require Facility Manager or Administrator."""
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in ['facility_manager', 'administrator'] or request.user.is_superuser

class CanInspectOrResolve(permissions.BasePermission):
    """Technicians and managers can update work items."""
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in ['technician', 'facility_manager', 'administrator'] or request.user.is_superuser
