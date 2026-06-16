from django import forms
from django.forms import formset_factory, inlineformset_factory
from .models import (
    Simulation, Supplier, Cargo, Customer, Plant, PlantInventory, APIConfiguration,
    SupplierDate, CustomerDate, Refinery, RefineryDate, SimulationComment
)


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plant Name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location (optional)'}),
        }


class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Simulation Name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class MasterSimulationForm(forms.ModelForm):
    """Form for admin to create/edit master simulation"""
    class Meta:
        model = Simulation
        fields = ['name', 'start_date', 'end_date', 'is_master', 'sap_api_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Master Simulation Name'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_master': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sap_api_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://sap-api.com/lng-data'}),
        }


class PlantInventoryForm(forms.ModelForm):
    class Meta:
        model = PlantInventory
        fields = ['plant', 'opening_inventory']
        widgets = {
            'plant': forms.Select(attrs={'class': 'form-control'}),
            'opening_inventory': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MT', 'step': '0.01'}),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'plant']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'}),
            'plant': forms.Select(attrs={'class': 'form-control'}),
        }


class SupplierDateForm(forms.ModelForm):
    class Meta:
        model = SupplierDate
        fields = ['from_date', 'to_date', 'daily_supply']
        widgets = {
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'daily_supply': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MT/day', 'step': '0.01'}),
        }


SupplierDateFormSet = inlineformset_factory(
    Supplier, SupplierDate,
    form=SupplierDateForm,
    extra=1,
    can_delete=True
)


class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['cargo_name', 'plant', 'delivery_date', 'amount']
        widgets = {
            'cargo_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cargo Name'}),
            'plant': forms.Select(attrs={'class': 'form-control'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MT', 'step': '0.01'}),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'plant']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'plant': forms.Select(attrs={'class': 'form-control'}),
        }


class CustomerDateForm(forms.ModelForm):
    class Meta:
        model = CustomerDate
        fields = ['from_date', 'to_date', 'daily_demand']
        widgets = {
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'daily_demand': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MT/day', 'step': '0.01'}),
        }


CustomerDateFormSet = inlineformset_factory(
    Customer, CustomerDate,
    form=CustomerDateForm,
    extra=1,
    can_delete=True
)


class APIConfigurationForm(forms.ModelForm):
    class Meta:
        model = APIConfiguration
        exclude = ['user', 'created_at']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'api_url': forms.URLInput(attrs={'class': 'form-control'}),
            'supplier_table': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., suppliers'}),
            'supplier_name_col': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_daily_supply_col': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_from_date_col': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_to_date_col': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo_table': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., cargos'}),
            'cargo_name_col': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo_date_col': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo_amount_col': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_table': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., customers'}),
            'customer_name_col': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_daily_demand_col': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_from_date_col': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_to_date_col': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RefineryForm(forms.ModelForm):
    class Meta:
        model = Refinery
        fields = ['name', 'plant']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Refinery Name'}),
            'plant': forms.Select(attrs={'class': 'form-control'}),
        }


class RefineryDateForm(forms.ModelForm):
    class Meta:
        model = RefineryDate
        fields = ['from_date', 'to_date', 'daily_refinery_supply']
        widgets = {
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'daily_refinery_supply': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MT/day', 'step': '0.01'}),
        }


RefineryDateFormSet = inlineformset_factory(
    Refinery, RefineryDate,
    form=RefineryDateForm,
    extra=1,
    can_delete=True
)


class SimulationCommentForm(forms.ModelForm):
    class Meta:
        model = SimulationComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your remarks or comments...',
                'rows': 3
            }),
        }


class JSONUploadForm(forms.Form):
    json_file = forms.FileField(
        label='JSON File',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.json'})
    )