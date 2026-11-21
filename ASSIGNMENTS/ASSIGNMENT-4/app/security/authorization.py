"""
Authorization enforcement, role hierarchy, and route protection.
"""

from typing import List

from fastapi import Depends, HTTPException, status

from app.models.user import User, UserRole
from app.security.authentication import get_current_user


class RoleChecker:
    """Dependency that checks if the current authenticated user has an allowed role."""

    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Role '{current_user.role.value}' lacks required permissions.",
            )
        return current_user


# Predefined role dependencies
require_admin = RoleChecker([UserRole.ADMINISTRATOR])
require_facility_manager_or_admin = RoleChecker([UserRole.ADMINISTRATOR, UserRole.FACILITY_MANAGER])
require_approver = RoleChecker(
    [UserRole.ADMINISTRATOR, UserRole.FACILITY_MANAGER, UserRole.DEPARTMENT_APPROVER]
)
require_technician_or_manager = RoleChecker(
    [UserRole.ADMINISTRATOR, UserRole.FACILITY_MANAGER, UserRole.MAINTENANCE_TECHNICIAN]
)
require_authenticated = RoleChecker(
    [
        UserRole.ADMINISTRATOR,
        UserRole.FACILITY_MANAGER,
        UserRole.MAINTENANCE_TECHNICIAN,
        UserRole.DEPARTMENT_APPROVER,
        UserRole.FACULTY_MEMBER,
        UserRole.STUDENT,
    ]
)


def can_approve_booking(user: User) -> bool:
    """Check if a user has authority to approve restricted bookings."""
    return user.role in {
        UserRole.ADMINISTRATOR,
        UserRole.FACILITY_MANAGER,
        UserRole.DEPARTMENT_APPROVER,
    }


def can_mutate_ticket(user: User) -> bool:
    """Check if a user has authority to mutate ticket states."""
    return user.role in {
        UserRole.ADMINISTRATOR,
        UserRole.FACILITY_MANAGER,
        UserRole.MAINTENANCE_TECHNICIAN,
    }
