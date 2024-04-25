from django import forms
from .models import *


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'
        widgets = {
            'maintenance_type': forms.RadioSelect()
        }


class ClaimsForm(forms.ModelForm):
    class Meta:
        model = Claims
        fields = '__all__'


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'
