import django_filters
from .models import Machine, Maintenance, Claims


class MachineFilter(django_filters.FilterSet):
    machine_model = django_filters.CharFilter(lookup_expr='icontains')
    engine_model = django_filters.CharFilter(lookup_expr='icontains')
    transmission_model = django_filters.CharFilter(lookup_expr='icontains')
    controlled_axle_model = django_filters.CharFilter(lookup_expr='icontains')
    driving_axle_model = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Machine
        fields = ['machine_model', 'engine_model', 'transmission_model', 'controlled_axle_model', 'driving_axle_model']


class MaintenanceFilter(django_filters.FilterSet):
    maintenance_type = django_filters.CharFilter(lookup_expr='icontains')
    machine_number = django_filters.CharFilter(lookup_expr='icontains')
    service_company = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'machine_number', 'service_company']


class ClaimsFilter(django_filters.FilterSet):
    failure_point = django_filters.CharFilter(lookup_expr='icontains')
    equipment_recovery_method = django_filters.CharFilter(lookup_expr='icontains')
    service_company = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Claims
        fields = ['failure_point', 'equipment_recovery_method', 'service_company']
