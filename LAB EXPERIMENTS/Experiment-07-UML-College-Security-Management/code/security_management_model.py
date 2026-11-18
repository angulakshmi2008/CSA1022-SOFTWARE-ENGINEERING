"""
Experiment 07: College Security Management System - UML Domain Model & Simulation
Student: Angulakshmi S (Reg No: 192524402)
Course: CSA10 - Software Engineering
Course Outcome: CO1

This script implements the full Object-Oriented architecture of the College Security
Management System, verifying classes, attributes, methods, salary calculations,
duty allocation, attendance recording, and leave approval workflows.
"""

from typing import List, Dict

class CampusLocation:
    def __init__(self, location_id: int, building_name: str, gate_no: int):
        self.location_id = location_id
        self.building_name = building_name
        self.gate_no = gate_no

    def __repr__(self):
        return f"{self.building_name} (Gate {self.gate_no})"

class DutySchedule:
    def __init__(self, duty_id: int, date: str, start_time: str, end_time: str, location: CampusLocation):
        self.duty_id = duty_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.status = "Scheduled"

    def update_duty_status(self, new_status: str):
        self.status = new_status

class Leave:
    def __init__(self, leave_id: int, security_id: int, leave_date: str, reason: str):
        self.leave_id = leave_id
        self.security_id = security_id
        self.leave_date = leave_date
        self.reason = reason
        self.status = "Pending"  # Pending, Approved, Rejected

    def approve(self):
        self.status = "Approved"

    def reject(self):
        self.status = "Rejected"

class Attendance:
    def __init__(self, attendance_id: int, security_id: int, date: str, check_in: str, check_out: str):
        self.attendance_id = attendance_id
        self.security_id = security_id
        self.date = date
        self.check_in = check_in
        self.check_out = check_out
        self.status = "Present"

class SecurityPersonnel:
    def __init__(self, security_id: int, name: str, phone: str, designation: str, basic_salary: float):
        self.security_id = security_id
        self.name = name
        self.phone = phone
        self.designation = designation
        self.basic_salary = basic_salary
        self.schedules: List[DutySchedule] = []
        self.leaves: List[Leave] = []
        self.attendance_records: List[Attendance] = []

    def view_schedule(self):
        print(f"\n[Security Guard: {self.name}] Assigned Duty Schedules:")
        for s in self.schedules:
            print(f"  • Date: {s.date} | Shift: {s.start_time} - {s.end_time} | Location: {s.location} | Status: {s.status}")

    def apply_leave(self, leave_id: int, date: str, reason: str) -> Leave:
        leave = Leave(leave_id, self.security_id, date, reason)
        self.leaves.append(leave)
        print(f"[Security Guard: {self.name}] Applied for Leave on {date}. Reason: '{reason}'")
        return leave

    def record_attendance(self, att_id: int, date: str, check_in: str, check_out: str):
        att = Attendance(att_id, self.security_id, date, check_in, check_out)
        self.attendance_records.append(att)
        print(f"[Attendance] Guard {self.name} checked in at {check_in}, checked out at {check_out} on {date}")

class Administrator:
    def __init__(self, admin_id: int, username: str):
        self.admin_id = admin_id
        self.username = username

    def assign_duty(self, guard: SecurityPersonnel, schedule: DutySchedule):
        guard.schedules.append(schedule)
        print(f"[Admin: {self.username}] Assigned Duty #{schedule.duty_id} to {guard.name} at {schedule.location}")

    def approve_leave(self, leave: Leave, approve: bool = True):
        if approve:
            leave.approve()
            print(f"[Admin: {self.username}] Approved Leave #{leave.leave_id} for Guard #{leave.security_id}")
        else:
            leave.reject()
            print(f"[Admin: {self.username}] Rejected Leave #{leave.leave_id}")

class Salary:
    def __init__(self, salary_id: int, guard: SecurityPersonnel, month: str):
        self.salary_id = salary_id
        self.guard = guard
        self.month = month
        self.basic_salary = guard.basic_salary
        self.total_duties = 0
        self.leave_count = 0
        self.final_salary = 0.0

    def calculate_salary(self, total_working_days: int = 30) -> float:
        self.total_duties = len(self.guard.attendance_records)
        # Count approved leaves
        self.leave_count = sum(1 for l in self.guard.leaves if l.status == "Approved")
        per_day_rate = self.basic_salary / total_working_days
        # Deduction for unpaid leaves or calculation based on attended duties
        deductions = self.leave_count * per_day_rate
        self.final_salary = max(0.0, self.basic_salary - deductions)
        return self.final_salary

    def print_pay_slip(self):
        print(f"\n========================================================")
        print(f"             COLLEGE SECURITY SALARY PAYSLIP            ")
        print(f"========================================================")
        print(f"Salary Slip ID   : SAL-{self.salary_id}")
        print(f"Month            : {self.month}")
        print(f"Security Guard   : {self.guard.name} (ID: {self.guard.security_id})")
        print(f"Designation      : {self.guard.designation}")
        print(f"Basic Monthly Pay: Rs. {self.basic_salary:,.2f}")
        print(f"Duties Attended  : {self.total_duties} shifts")
        print(f"Approved Leaves  : {self.leave_count} days")
        print(f"Leave Deductions : Rs. {(self.basic_salary - self.final_salary):,.2f}")
        print(f"--------------------------------------------------------")
        print(f"NET PAYABLE SALARY: Rs. {self.final_salary:,.2f}")
        print(f"========================================================")

def run_simulation():
    print("==================================================================")
    print("      COLLEGE SECURITY MANAGEMENT SYSTEM - MODEL EXECUTION        ")
    print("==================================================================")

    # 1. Setup Admin and Locations
    admin = Administrator(1, "ChiefSecurityOfficer")
    loc_main_gate = CampusLocation(101, "Main Entrance Gate", 1)
    loc_library = CampusLocation(102, "Central Library Block", 3)
    loc_hostel = CampusLocation(103, "Student Residential Block", 5)

    # 2. Register Security Personnel
    guard1 = SecurityPersonnel(501, "M. Thangaraj", "+91-9444123456", "Senior Guard", 24000.0)
    guard2 = SecurityPersonnel(502, "K. Selvam", "+91-9444654321", "Patrol Officer", 22000.0)

    # 3. Duty Allocation by Administrator
    sched1 = DutySchedule(1001, "2026-11-19", "06:00 AM", "02:00 PM", loc_main_gate)
    sched2 = DutySchedule(1002, "2026-11-19", "02:00 PM", "10:00 PM", loc_library)
    admin.assign_duty(guard1, sched1)
    admin.assign_duty(guard2, sched2)

    # 4. Guard views duty schedule
    guard1.view_schedule()

    # 5. Record Attendance
    guard1.record_attendance(201, "2026-11-19", "05:55 AM", "02:05 PM")
    sched1.update_duty_status("Completed")

    # 6. Leave Application & Approval
    leave1 = guard1.apply_leave(301, "2026-11-25", "Medical checkup and personal leave")
    admin.approve_leave(leave1, approve=True)

    # 7. Salary Processing by Accounts Officer at Month End
    sal = Salary(701, guard1, "November 2026")
    sal.calculate_salary(total_working_days=30)
    sal.print_pay_slip()

if __name__ == "__main__":
    run_simulation()
