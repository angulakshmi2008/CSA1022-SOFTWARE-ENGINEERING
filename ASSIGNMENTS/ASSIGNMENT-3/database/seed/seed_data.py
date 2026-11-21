"""
Comprehensive Seed Data Script for Smart Campus Platform.
Populates 6 campuses, 6 user roles, facilities, SLA policies, initial bookings,
tickets, sensor events, and durable integration intents.
"""

import os
import sys
from pathlib import Path
from datetime import timedelta

# Ensure backend directory is in python path
BASE_DIR = Path(__file__).resolve().parent.parent.parent / 'backend'
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from campuses.models import Campus
from facilities.models import Facility, FacilityType
from accounts.models import UserRole
from bookings.models import Booking, BookingStatus
from equipment_loans.models import EquipmentLoan, LoanStatus
from maintenance.models import Ticket, TicketSource, TicketCategory, PriorityLevel, TicketStatus, InspectionComment, SLAPolicy
from sensor_events.models import SensorEvent
from approvals.models import Approval, RequestType, ApprovalDecision
from integrations.models import IntegrationIntent, IntentStatus
from audit.models import AuditEvent

User = get_user_model()

def seed_database():
    print("--- Starting Database Seeding ---")

    # 1. Seed 6 Campuses (Satisfies Task 6 requirement)
    campuses_data = [
        {"code": "MAIN", "name": "Main University Campus", "city": "Chennai", "timezone": "Asia/Kolkata"},
        {"code": "MED", "name": "Medical Sciences Campus", "city": "Chennai", "timezone": "Asia/Kolkata"},
        {"code": "ENG", "name": "Engineering City Campus", "city": "Bengaluru", "timezone": "Asia/Kolkata"},
        {"code": "NRP", "name": "North Research Park", "city": "Hyderabad", "timezone": "Asia/Kolkata"},
        {"code": "SHS", "name": "South Health Sciences Campus", "city": "Kochi", "timezone": "Asia/Kolkata"},
        {"code": "CIH", "name": "Coastal Innovation Hub", "city": "Visakhapatnam", "timezone": "Asia/Kolkata"},
    ]

    campuses = {}
    for cdata in campuses_data:
        campus, created = Campus.objects.get_or_create(code=cdata['code'], defaults=cdata)
        campuses[cdata['code']] = campus
        print(f"[{'CREATED' if created else 'EXISTS'}] Campus: {campus.name} ({campus.code})")

    # 2. Seed Users across all 6 Roles
    users_data = [
        {"username": "admin", "email": "admin@campus.edu", "role": UserRole.ADMINISTRATOR, "dept": "Campus IT Services", "campus": campuses['MAIN'], "first_name": "System", "last_name": "Administrator", "is_superuser": True, "is_staff": True},
        {"username": "approver.dr.kumar", "email": "kumar.approver@campus.edu", "role": UserRole.DEPARTMENT_APPROVER, "dept": "Dean of Academic Affairs", "campus": campuses['MAIN'], "first_name": "Dr. Ramesh", "last_name": "Kumar"},
        {"username": "manager.priya", "email": "priya.facilities@campus.edu", "role": UserRole.FACILITY_MANAGER, "dept": "Campus Operations & Facilities", "campus": campuses['MAIN'], "first_name": "Priya", "last_name": "Nair"},
        {"username": "tech.rajesh", "email": "rajesh.maintenance@campus.edu", "role": UserRole.TECHNICIAN, "dept": "HVAC & Electrical Maintenance", "campus": campuses['MAIN'], "first_name": "Rajesh", "last_name": "Kannan"},
        {"username": "tech.vikram", "email": "vikram.maintenance@campus.edu", "role": UserRole.TECHNICIAN, "dept": "Plumbing & Mechanical Services", "campus": campuses['ENG'], "first_name": "Vikram", "last_name": "Singh"},
        {"username": "faculty.dr.anand", "email": "anand.faculty@campus.edu", "role": UserRole.FACULTY, "dept": "Robotics & Automation Engineering", "campus": campuses['MAIN'], "first_name": "Dr. Anand", "last_name": "Subramanian"},
        {"username": "student.arun", "email": "arun.student@campus.edu", "role": UserRole.STUDENT, "dept": "Computer Science & Engineering", "campus": campuses['MAIN'], "first_name": "Arun", "last_name": "Sundaram"},
        {"username": "student.meera", "email": "meera.student@campus.edu", "role": UserRole.STUDENT, "dept": "Biomedical Sciences", "campus": campuses['MED'], "first_name": "Meera", "last_name": "Venkatesh"},
    ]

    users = {}
    for udata in users_data:
        username = udata.pop('username')
        password = 'Password@123'
        dept = udata.pop('dept')
        campus = udata.pop('campus')
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': udata.get('email'),
                'role': udata.get('role'),
                'department': dept,
                'campus': campus,
                'first_name': udata.get('first_name', ''),
                'last_name': udata.get('last_name', ''),
                'is_superuser': udata.get('is_superuser', False),
                'is_staff': udata.get('is_staff', False),
            }
        )
        if created:
            user.set_password(password)
            user.save()
        Token.objects.get_or_create(user=user)
        users[username] = user
        print(f"[{'CREATED' if created else 'EXISTS'}] User: {user.username} ({user.get_role_display()})")

    # 3. Seed Facilities
    facilities_data = [
        {"campus": campuses['MAIN'], "name": "Advanced Robotics & AI Research Lab", "code": "MAIN-ROBO-101", "facility_type": FacilityType.RESEARCH_LAB, "capacity": 30, "is_restricted": True, "location_details": "Block B, Level 3, Room 302"},
        {"campus": campuses['MAIN'], "name": "Alan Turing Computer Laboratory", "code": "MAIN-CS-LAB-01", "facility_type": FacilityType.COMPUTER_LAB, "capacity": 60, "is_restricted": False, "location_details": "Block A, Ground Floor"},
        {"campus": campuses['MAIN'], "name": "Sir C.V. Raman Auditorium", "code": "MAIN-AUD-RAMAN", "facility_type": FacilityType.LECTURE_HALL, "capacity": 250, "is_restricted": False, "location_details": "Central Academic Plaza"},
        {"campus": campuses['MED'], "name": "Bio-Safety Containment Lab Level 3", "code": "MED-BSL3-01", "facility_type": FacilityType.RESEARCH_LAB, "capacity": 15, "is_restricted": True, "location_details": "Medical Research Tower, Wing C"},
        {"campus": campuses['ENG'], "name": "Mechatronics & IoT Testing Hub", "code": "ENG-IOT-204", "facility_type": FacilityType.COMPUTER_LAB, "capacity": 45, "is_restricted": False, "location_details": "Innovation Block, Level 2"},
        {"campus": campuses['NRP'], "name": "Nanotechnology Cleanroom 100", "code": "NRP-NANO-CR1", "facility_type": FacilityType.RESEARCH_LAB, "capacity": 10, "is_restricted": True, "location_details": "Cleanroom Complex, Sector 4"},
    ]

    facilities = {}
    for fdata in facilities_data:
        code = fdata['code']
        fac, created = Facility.objects.get_or_create(code=code, defaults=fdata)
        facilities[code] = fac
        print(f"[{'CREATED' if created else 'EXISTS'}] Facility: {fac.name} [{fac.code}] (Restricted={fac.is_restricted})")

    # 4. Seed SLA Policies
    for campus in campuses.values():
        for prio, r_mins in [('M1', 120), ('M2', 240), ('M3', 480), ('M4', 1440)]:
            SLAPolicy.objects.get_or_create(
                campus=campus,
                category='all',
                priority=prio,
                defaults={
                    'response_minutes': r_mins // 4,
                    'resolution_minutes': r_mins,
                    'version': 1
                }
            )

    # 5. Seed Demonstration Bookings
    now = timezone.now()
    b1_start = now.replace(minute=0, second=0, microsecond=0) + timedelta(days=1, hours=2)
    b1_end = b1_start + timedelta(hours=2)

    b1, created = Booking.objects.get_or_create(
        facility=facilities['MAIN-CS-LAB-01'],
        start_at=b1_start,
        end_at=b1_end,
        defaults={
            'requester': users['faculty.dr.anand'],
            'status': BookingStatus.CONFIRMED,
            'purpose': "Distributed Systems Lab Practical Session",
            'request_key': "seed-req-booking-001",
            'version': 1
        }
    )
    print(f"[{'CREATED' if created else 'EXISTS'}] Booking: #{b1.id} for {b1.facility.code}")

    # Seed Pending Restricted Booking
    b2_start = now.replace(minute=0, second=0, microsecond=0) + timedelta(days=2, hours=4)
    b2_end = b2_start + timedelta(hours=3)
    b2, created = Booking.objects.get_or_create(
        facility=facilities['MAIN-ROBO-101'],
        start_at=b2_start,
        end_at=b2_end,
        defaults={
            'requester': users['faculty.dr.anand'],
            'status': BookingStatus.REQUESTED,
            'purpose': "Autonomous Drone Swarm Navigation Protocol Test",
            'request_key': "seed-req-booking-002",
            'version': 1
        }
    )
    print(f"[{'CREATED' if created else 'EXISTS'}] Restricted Booking #{b2.id} awaiting approval.")

    # 6. Seed Maintenance Tickets
    t1, created = Ticket.objects.get_or_create(
        title="High Temperature Chiller Fault in Server Room B",
        defaults={
            'campus': campuses['MAIN'],
            'facility': facilities['MAIN-CS-LAB-01'],
            'source': TicketSource.SENSOR_EVENT,
            'description': "Ambient temperature sensor HVAC-TEMP-UNIT-04 breached critical threshold (31.2°C). Server hardware thermal shutdown risk.",
            'category': TicketCategory.HVAC,
            'impact': 'high',
            'urgency': 'high',
            'priority': PriorityLevel.M1,
            'triage_explanation': "[Explainable Triage] Matched 'chiller', 'temperature' keywords -> HVAC. Impact=HIGH, Urgency=HIGH -> M1 Critical (2h SLA).",
            'status': TicketStatus.ASSIGNED,
            'assignee': users['tech.rajesh'],
            'sla_due_at': now + timedelta(hours=2),
            'version': 1
        }
    )
    print(f"[{'CREATED' if created else 'EXISTS'}] Maintenance Ticket: #{t1.id} [{t1.priority}]")

    # Add Inspection Comment
    InspectionComment.objects.get_or_create(
        ticket=t1,
        author=users['tech.rajesh'],
        comment_type=InspectionComment.CommentType.INSPECTION,
        defaults={
            'notes': "Inspected primary condenser unit. Compressor discharge valve has abnormal pressure oscillation. Preparing coolant recharge.",
            'evidence_ref': "GAUGE-PSI-340"
        }
    )

    # 7. Seed Sensor Event
    SensorEvent.objects.get_or_create(
        source_id="HVAC-TEMP-UNIT-04",
        event_id="evt-seed-1001-init",
        defaults={
            'metric': "temperature_celsius",
            'value': 31.2,
            'observed_at': now - timedelta(minutes=45),
            'ticket': t1
        }
    )

    # 8. Seed Equipment Loan
    EquipmentLoan.objects.get_or_create(
        asset_code="ASSET-OSC-042",
        defaults={
            'requester': users['student.arun'],
            'asset_name': "Digital Storage Oscilloscope DS1054Z (4-Channel)",
            'start_at': now + timedelta(days=1),
            'end_at': now + timedelta(days=3),
            'status': LoanStatus.PENDING_APPROVAL,
            'purpose': "Robotics capstone motor pulse-width modulation analysis"
        }
    )

    # 9. Seed Integration Intent (Outbox Pattern)
    IntegrationIntent.objects.get_or_create(
        correlation_key=f"CAMP-318-TKT-{t1.id}",
        defaults={
            'ticket': t1,
            'operation': "create_developer_issue",
            'status': IntentStatus.CONFIRMED,
            'attempts': 1,
            'external_id': f"GH-ISSUE-{t1.id}-PROD"
        }
    )

    # 10. Seed Initial Audit Events
    AuditEvent.objects.get_or_create(
        entity_type="CampusPlatform",
        entity_id=1,
        action="SYSTEM_INITIALIZE",
        defaults={
            'actor': users['admin'],
            'before_state': None,
            'after_state': {"system_status": "ONLINE", "campuses_loaded": 6, "version": "1.0.0"},
            'ip_address': "127.0.0.1"
        }
    )

    print("--- Database Seeding Completed Successfully ---")

if __name__ == '__main__':
    seed_database()
