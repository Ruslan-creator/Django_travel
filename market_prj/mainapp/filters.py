import django_filters

from mainapp.models import Accommodation


class AccommodationFilter(django_filters.FilterSet):
    """
    Can assert field and lookups for filter
    """
    q = django_filters.CharFilter(field_name='region__name', lookup_expr='icontains')

    class Meta:
        model = Accommodation
        fields = {
            'price': ['lte', 'gte'],
            'rating': ['exact']
        }
