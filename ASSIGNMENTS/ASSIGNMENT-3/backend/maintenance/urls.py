from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, SLAPolicyViewSet

router = DefaultRouter()
router.register(r'sla-policies', SLAPolicyViewSet, basename='sla-policy')
router.register(r'', TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]
