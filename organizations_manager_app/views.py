from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
import logging
from .models import Organization, Industry, OwnershipStructure
from .serializers import OrganizationSerializer, OwnershipStructureSerializer

logger = logging.getLogger(__name__)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all().prefetch_related('ownership_structures', 'industry')
    serializer_class = OrganizationSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def filter(self, request):
        # Validate and normalize parameters
        params = {
            'name': request.GET.get('name', '').strip(),
            'type': request.GET.get('type', '').strip().lower(),
            'ownership': request.GET.getlist('ownership', []),
            'industry': request.GET.get('industry', '').split(' - ')[0].strip().upper(),
            'geo_scope': request.GET.get('geoScope', '').strip().lower(),
            'governance': request.GET.get('governance', '').strip().lower(),
        }

        logger.info(f"Filter request received with params: {params}")

        # Build query with validation
        query = Q()
        errors = []

        # Name filter (partial match)
        if params['name']:
            query &= Q(name__icontains=params['name'])

        # Type filter (exact match)
        if params['type']:
            query &= Q(type__iexact=params['type'])

        # Ownership filter (multi-select)
        if params['ownership']:
            try:
                valid_ids = OwnershipStructure.objects.filter(
                    name__in=params['ownership']
                ).values_list('id', flat=True)
                
                if valid_ids:
                    query &= Q(ownership_structures__id__in=valid_ids)
                else:
                    errors.append(f"No matching ownership structures found for: {params['ownership']}")
            except Exception as e:
                logger.error(f"Ownership filter error: {str(e)}")
                errors.append("Invalid ownership structure filter")

        # Industry filter (NACE code exact match)
        if params['industry']:
            try:
                industry = Industry.objects.get(nace_code__iexact=params['industry'])
                print(industry)
                query &= Q(industry=industry)
            except Industry.DoesNotExist:
                errors.append(f"Invalid industry code: {params['industry']}")
            except Industry.MultipleObjectsReturned:
                errors.append(f"Multiple industries found for code: {params['industry']}")

        # Geo Scope filter (exact match)
        if params['geo_scope']:
            query &= Q(geo_scope__iexact=params['geo_scope'])

        # Governance filter (exact match)
        if params['governance']:
            query &= Q(governance__iexact=params['governance'])


        organizations = Organization.objects.filter(query).distinct()

        serializer = self.get_serializer(organizations, many=True)
        response_data = {
            'count': organizations.count(),
            'results': serializer.data
        }

        if errors:
            response_data['warnings'] = errors
            logger.warning(f"Filter completed with warnings: {errors}")

        return Response(response_data)


class OwnershipStructureViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing ownership structures.
    """
    queryset = OwnershipStructure.objects.all()
    serializer_class = OwnershipStructureSerializer