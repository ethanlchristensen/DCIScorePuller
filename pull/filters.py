import django_filters
from django.db.models import Q
from django_filters import FilterSet

from .models import Show


class ShowFilter(FilterSet):
    query = django_filters.CharFilter(method="query_filter", label="Search Competitions or Corps")

    class Meta:
        model = Show
        fields = ["query"]

    def query_filter(self, queryset, name, value):
        return queryset.filter(
            Q(competition__competition_name_original__icontains=value)
            | Q(corp__name__icontains=value)
            | Q(competition__competition_date_as_string__icontains=value)
        )
