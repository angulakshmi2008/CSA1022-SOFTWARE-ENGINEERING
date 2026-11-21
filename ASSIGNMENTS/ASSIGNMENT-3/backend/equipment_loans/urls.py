from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentLoanViewSet

router = DefaultRouter()
router.register(r'', EquipmentLoanViewSet, basename='equipment-loan')

urlpatterns = [
    path('', include(router.urls)),
]
