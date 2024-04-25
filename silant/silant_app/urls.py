from django.urls import path, include
from rest_framework import routers

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', MachineSearchView.as_view(), name='machine_search'),

    path('machines/', MachineListView.as_view(), name='machine_list'),
    path('machine/<pk>/detail', MachineDetailView.as_view(), name='machine_detail'),
    path('machine/create', MachineCreateView.as_view(), name='machine_create'),
    path('machine/<pk>/update', MachineUpdateView.as_view(), name='machine_update'),
    path('machine/<pk>/delete', MachineDeleteView.as_view(), name='machine_delete'),
    path('machine/<pk>/description/<attribute>', MachineDescriptionView.as_view(), name='machine_description'),

    path('maintenances/', MaintenanceListView.as_view(), name='maintenance_list'),
    path('maintenance/create', MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('maintenance/<pk>/update', MaintenanceUpdateView.as_view(), name='maintenance_update'),
    path('maintenance/<pk>/delete', MaintenanceDeleteView.as_view(), name='maintenance_delete'),
    path('car/<pk>/maintenances', CarMaintenanceListView.as_view(), name='car_maintenance'),
    path('maintenance/<pk>/description/<attribute>', MaintenanceDescriptionView.as_view(),
         name='maintenance_description'),

    path('claims/', ClaimsListView.as_view(), name='claims_list'),
    path('claims/create', ClaimsCreateView.as_view(), name='claims_create'),
    path('claims/<pk>/update', ClaimsUpdateView.as_view(), name='claims_update'),
    path('claims/<pk>/delete', ClaimsDeleteView.as_view(), name='claims_delete'),
    path('car/<pk>/claims', CarClaimsListView.as_view(), name='car_claims'),
    path('claims/<pk>/description/<attribute>', ClaimsDescriptionView.as_view(), name='claims_description'),
]
