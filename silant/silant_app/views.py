from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import MachineFilter
from .forms import MachineForm, MaintenanceForm, ClaimsForm
# from .forms import PostForm
from .models import *
from .serializer import *


def create_groups(sender, **kwargs):
    if not Group.objects.create(name='Clients'):
        Group.objects.create(name='Clients')

    if not Group.objects.create(name='Service companies'):
        Group.objects.create(name='Service companies')

    if not Group.objects.create(name='Managers'):
        Group.objects.create(name='Managers')


def is_client(user):
    return user.groups.filter(name='Clients').exists()


def is_service_organization(user):
    return user.groups.filter(name='Service companies').exists()


def is_manager(user):
    return user.groups.filter(name='Managers').exists()


@api_view(['GET'])
@login_required
@user_passes_test(is_client)
def machine_list(request):
    cars = Machine.objects.all()
    serializer = MachineSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@login_required
@user_passes_test(is_client)
def car_detail(request):
    machine_number = request.GET.get('machine_number')
    try:
        car = Machine.objects.get(machine_number=machine_number)
        serializer = MachineSerializer(car)
        return Response(serializer.data)
    except Machine.DoesNotExist:
        message = "Данных о машине с таким заводским номером нет в системе."
        return Response({'message': message})


@api_view(['GET'])
@login_required
@user_passes_test(is_service_organization)
def service_list(request, id):
    try:
        car = Machine.objects.get(id=id)
        maintenances = Maintenance.objects.filter(car=car)
        serializer = MaintenanceSerializer(maintenances, many=True)
        return Response(serializer.data)
    except Machine.DoesNotExist:
        message = "Данных о машине с таким идентификатором нет в системе."
        return Response({'message': message})


@api_view(['GET'])
@login_required
@user_passes_test(is_manager)
def claim_list(request, id):
    try:
        car = Machine.objects.get(id=id)
        claims = Claims.objects.filter(car=car)
        serializer = ClaimsSerializer(claims, many=True)
        return Response(serializer.data)
    except Machine.DoesNotExist:
        message = "Данных о машине с таким идентификатором нет в системе."
        return Response({'message': message})


def login(request):
    # ToDo: Put actual template here
    return render(request, 'login.html')


class HomeView(TemplateView):
    template_name = 'index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('machine_list')
        else:
            return redirect('machine_search')


class MachineSearchView(ListView):
    model = Machine
    template_name = 'machine_search.html'
    queryset = Machine.objects.all()


class MachineListView(LoginRequiredMixin, ListView):
    model = Machine
    template_name = 'machine_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Machine.objects.all()
        else:
            user = User.objects.get(pk=self.request.user.pk)
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.is_service:
                    return Machine.objects.filter(service_company=profile.service_company)
            except:
                return Machine.objects.filter(client=user)


class MachineDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'silant_app.view_machine'
    model = Machine
    template_name = 'machine_view.html'
    context_object_name = 'obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MachineCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'silant_app.add_machine'
    model = Machine
    form_class = MachineForm
    template_name = 'machine_create.html'
    success_url = reverse_lazy('machine_list')


class MachineUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'silant_app.change_machine'
    model = Machine
    form_class = MachineForm
    template_name = 'machine_update.html'
    success_url = reverse_lazy('machine_list')


class MachineDescriptionView(TemplateView):
    template_name = 'modal_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = Machine.objects.get(pk=self.kwargs["pk"])
        attribute = context['attribute']
        if attribute == 'machine_model':
            context['attribute'] = car.machine_model.name
            context['description'] = car.machine_model.description
        elif attribute == 'engine_model':
            context['attribute'] = car.engine_model.name
            context['description'] = car.engine_model.description
        elif attribute == 'transmission_model':
            context['attribute'] = car.transmission_model.name
            context['description'] = car.transmission_model.description
        elif attribute == 'driving_axle':
            context['attribute'] = car.driving_axle_model.name
            context['description'] = car.driving_axle_model.description
        elif attribute == 'controlled_axle':
            context['attribute'] = car.controlled_axle_model.name
            context['description'] = car.controlled_axle_model.description
        elif attribute == 'specification':
            context['attribute'] = 'Комплектация'
            context['description'] = car.specification
        elif attribute == 'service_company':
            context['attribute'] = car.service_company.name
            context['description'] = car.service_company.description
        return context


class MachineDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'silant_app.delete_machine'
    model = Machine
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('machine_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'machine'
        return context


class MaintenanceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'silant_app.view_maintenance'
    model = Maintenance
    template_name = 'maintenance_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Maintenance.objects.all()
        else:
            user = User.objects.get(pk=self.request.user.pk)
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.is_service:
                    return Maintenance.objects.filter(maintenance_provider=profile.service_company)
            except:
                return Maintenance.objects.filter(machine__client=user)


class MaintenanceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'silant_app.add_maintenance'
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance_create.html'
    success_url = reverse_lazy('maintenance_list')


class MaintenanceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'silant_app.change_maintenance'
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance_update.html'
    success_url = reverse_lazy('maintenance_list')


class MaintenanceDeleteView(DeleteView):
    model = Maintenance
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('maintenance_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'maintenance'
        return context


class ClaimsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'silant_app.view_claims'
    model = Claims
    template_name = 'claims_list.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return Claims.objects.all()
        else:
            user = User.objects.get(pk=self.request.user.pk)
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.is_service:
                    return Claims.objects.filter(service_company=profile.service_company)
            except:
                return Claims.objects.filter(machine__client=user)


class ClaimsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'silant_app.add_claims'
    model = Claims
    form_class = ClaimsForm
    template_name = 'claims_create.html'
    success_url = reverse_lazy('claims_list')


class ClaimsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'silant_app.change_claims'
    model = Claims
    form_class = ClaimsForm
    template_name = 'claims_update.html'
    success_url = reverse_lazy('claims_list')


class ClaimsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'silant_app.delete_claims'
    model = Claims
    template_name_suffix = '_confirm_delete'
    success_url = reverse_lazy('claims_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'claims'
        return context


class CarMaintenanceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'silant_app.view_maintenance'
    model = Maintenance
    template_name = 'car_maintenance.html'

    def get_queryset(self):
        machine = Machine.objects.get(pk=self.kwargs["pk"])
        return Maintenance.objects.filter(machine=machine)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["machine"] = Machine.objects.get(pk=self.kwargs["pk"])
        return context


class CarClaimsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'silant_app.view_maintenance'
    model = Claims
    template_name = 'car_claims.html'

    def get_queryset(self):
        machine = Machine.objects.get(pk=self.kwargs["pk"])
        return Claims.objects.filter(machine=machine)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["machine"] = Machine.objects.get(pk=self.kwargs["pk"])
        return context


class MaintenanceDescriptionView(TemplateView):
    template_name = 'modal_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maintenance = Maintenance.objects.get(pk=self.kwargs["pk"])
        attribute = context['attribute']
        if attribute == 'type':
            context['attribute'] = maintenance.maintenance_type.name
            context['description'] = maintenance.maintenance_type.description
        elif attribute == 'maintenance_provider':
            context['attribute'] = maintenance.maintenance_provider.name
            context['description'] = maintenance.maintenance_provider.description
        return context


class ClaimsDescriptionView(TemplateView):
    template_name = 'modal_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        complaint = Claims.objects.get(pk=self.kwargs["pk"])
        attribute = context['attribute']
        if attribute == 'failure_point':
            context['attribute'] = complaint.failure_point.name
            context['description'] = complaint.failure_point.description
        elif attribute == 'equipment_recovery_method':
            context['attribute'] = complaint.equipment_recovery_method.name
            context['description'] = complaint.equipment_recovery_method.description
        elif attribute == 'service_company':
            context['attribute'] = complaint.service_company.name
            context['description'] = complaint.service_company.description
        return context
