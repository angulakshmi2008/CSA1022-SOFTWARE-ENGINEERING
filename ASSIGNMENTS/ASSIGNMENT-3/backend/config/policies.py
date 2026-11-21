"""
System Operating Policies and SLA Configuration for Smart Campus Platform.
Approved university rules for facility durations, priority matrices, and SLA timelines.
"""

# Maximum permitted reservation duration in hours for standard bookings
# Policy Ref: POL-FAC-2026-01 (Approved baseline: 4 hours)
# Extensions up to 8 hours require Department Approver sign-off via US03 workflow.
MAX_BOOKING_DURATION_HOURS = 4
MAX_EXTENDED_BOOKING_DURATION_HOURS = 8

# Minimum advance booking buffer in minutes
MIN_ADVANCE_BOOKING_MINUTES = 15

# Default operational operating hours (24h format UTC)
OPERATING_HOUR_START = 6
OPERATING_HOUR_END = 23

# Maintenance Triage SLA Resolution Deadlines (in minutes)
SLA_RESOLUTION_MINUTES = {
    'M1': 120,   # Critical: 2 hours
    'M2': 240,   # High: 4 hours
    'M3': 480,   # Medium: 8 hours
    'M4': 1440,  # Low: 24 hours
}

# Maintenance Triage SLA Initial Response Deadlines (in minutes)
SLA_RESPONSE_MINUTES = {
    'M1': 15,
    'M2': 30,
    'M3': 60,
    'M4': 120,
}

# Sensor fault detection thresholds
SENSOR_THRESHOLDS = {
    'temperature_celsius': {
        'high_critical': 30.0,
        'high_warning': 26.0,
        'low_warning': 16.0,
    },
    'vibration_hz': {
        'high_critical': 60.0,
        'high_warning': 45.0,
    },
    'power_kw': {
        'high_critical': 50.0,
    }
}
