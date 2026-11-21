from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorEventViewSet, SensorEventIngestView

router = DefaultRouter()
router.register(r'history', SensorEventViewSet, basename='sensor-event')

urlpatterns = [
    path('', SensorEventIngestView.as_view(), name='sensor-ingest'),
    path('', include(router.urls)),
]
