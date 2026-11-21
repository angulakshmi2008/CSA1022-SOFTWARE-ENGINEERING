"""
Master URL routing configuration for Smart Campus Platform.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.db import connection

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for Docker Compose and Load Balancer readiness probes.
    Verifies database connectivity and returns instance identity.
    """
    db_status = "unhealthy"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
            if row and row[0] == 1:
                db_status = "healthy"
    except Exception as exc:
        db_status = f"database_error: {str(exc)}"

    is_healthy = db_status == "healthy"
    status_code = 200 if is_healthy else 503

    return Response({
        "status": "healthy" if is_healthy else "unhealthy",
        "database": db_status,
        "instance_id": settings.INSTANCE_ID,
        "environment": "production" if not settings.DEBUG else "development",
        "service": "smart-campus-api",
        "version": "1.0.0"
    }, status=status_code)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', health_check, name='health-check'),
    path('api/auth/', include('accounts.urls')),
    path('api/campuses/', include('campuses.urls')),
    path('api/facilities/', include('facilities.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/equipment-loans/', include('equipment_loans.urls')),
    path('api/tickets/', include('maintenance.urls')),
    path('api/sensor-events/', include('sensor_events.urls')),
    path('api/approvals/', include('approvals.urls')),
    path('api/integration-intents/', include('integrations.urls')),
    path('api/audit-events/', include('audit.urls')),
    path('api/dashboard/', include('maintenance.dashboard_urls')),
]
