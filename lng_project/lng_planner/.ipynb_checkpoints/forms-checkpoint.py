from django import forms
from .models import Simulation, Supplier, Cargo, Customer, Plant, PlantInventory, APIConfiguration


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
        fields = ['name', 'plant', 'daily_supply', 'from_date', 'to_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Name'}),
            'plant': forms.Select(attrs={'class': 'form-control'}),
            'daily_supply': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MT/day', 'step': '0.01'}),
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


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
        fields = ['name', 'plant', 'daily_demand', 'from_date', 'to_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'plant': forms.Select(attrs={'class': 'form-control'}),
            'daily_demand': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'MT/day', 'step': '0.01'}),
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


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


class JSONUploadForm(forms.Form):
    json_file = forms.FileField(
        label='JSON File',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.json'})
    )