from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    STUDENT = 'student', 'Student'
    FACULTY = 'faculty', 'Faculty Member'
    FACILITY_MANAGER = 'facility_manager', 'Facility Manager'
    TECHNICIAN = 'technician', 'Maintenance Technician'
    DEPARTMENT_APPROVER = 'department_approver', 'Department Approver'
    ADMINISTRATOR = 'administrator', 'System Administrator'

class User(AbstractUser):
    role = models.CharField(
        max_length=30,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        help_text="Role determining operational permissions across the platform."
    )
    campus = models.ForeignKey(
        'campuses.Campus',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    department = models.CharField(max_length=100, default='General Campus')
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'auth_user_custom'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_student(self):
        return self.role == UserRole.STUDENT

    @property
    def is_faculty(self):
        return self.role == UserRole.FACULTY

    @property
    def is_facility_manager(self):
        return self.role == UserRole.FACILITY_MANAGER or self.is_superuser

    @property
    def is_technician(self):
        return self.role == UserRole.TECHNICIAN

    @property
    def is_department_approver(self):
        return self.role == UserRole.DEPARTMENT_APPROVER or self.is_superuser

    @property
    def is_administrator(self):
        return self.role == UserRole.ADMINISTRATOR or self.is_superuser
