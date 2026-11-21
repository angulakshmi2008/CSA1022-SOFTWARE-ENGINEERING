from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Facility
from .serializers import FacilitySerializer

class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.filter(is_active=True).select_related('campus')
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code', 'facility_type', 'campus__name']

    def get_queryset(self):
        qs = super().get_queryset()
        campus = self.request.query_params.get('campus')
        facility_type = self.request.query_params.get('type')
        capacity_min = self.request.query_params.get('capacity_min')
        is_restricted = self.request.query_params.get('restricted')

        if campus:
            qs = qs.filter(campus_id=campus)
        if facility_type:
            qs = qs.filter(facility_type=facility_type)
        if capacity_min:
            try:
                qs = qs.filter(capacity__gte=int(capacity_min))
            except ValueError:
                pass
        if is_restricted is not None:
            qs = qs.filter(is_restricted=is_restricted.lower() in ('true', '1'))
        return qs
