from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IntegrationIntentViewSet

router = DefaultRouter()
router.register(r'', IntegrationIntentViewSet, basename='integration-intent')

urlpatterns = [
    path('', include(router.urls)),
]
