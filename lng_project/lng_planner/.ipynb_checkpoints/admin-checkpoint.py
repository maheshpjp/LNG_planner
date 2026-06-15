from django.contrib import admin
from .models import Simulation, Supplier, Cargo, Customer, Plant, PlantInventory, APIConfiguration


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'created_at']
    search_fields = ['name', 'location']


class PlantInventoryInline(admin.TabularInline):
    model = PlantInventory
    extra = 1
    fields = ['plant', 'opening_inventory']


class SupplierInline(admin.TabularInline):
    model = Supplier
    extra = 1
    fields = ['name', 'plant', 'daily_supply', 'from_date', 'to_date']


class CargoInline(admin.TabularInline):
    model = Cargo
    extra = 1
    fields = ['cargo_name', 'plant', 'delivery_date', 'amount']


class CustomerInline(admin.TabularInline):
    model = Customer
    extra = 1
    fields = ['name', 'plant', 'daily_demand', 'from_date', 'to_date']


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'start_date', 'end_date', 'is_master', 'is_active', 'last_sap_sync', 'updated_at']
    list_filter = ['is_active', 'is_master', 'created_at', 'user']
    search_fields = ['name', 'user__username']
    date_hierarchy = 'created_at'
    inlines = [PlantInventoryInline, SupplierInline, CargoInline, CustomerInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'is_active', 'is_master')
        }),
        ('Planning Parameters', {
            'fields': ('start_date', 'end_date')
        }),
        ('SAP Integration (Master Only)', {
            'fields': ('sap_api_url', 'last_sap_sync'),
            'classes': ('collapse',),
            'description': 'These fields are only used for master simulations'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_sap_sync']
    
    def get_readonly_fields(self, request, obj=None):
        """Make last_sap_sync always readonly"""
        readonly = list(self.readonly_fields)
        if obj and obj.is_master:
            # When editing master, show last_sap_sync as readonly
            pass
        return readonly


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'plant', 'simulation', 'daily_supply', 'from_date', 'to_date']
    list_filter = ['simulation', 'plant', 'created_at']
    search_fields = ['name', 'simulation__name', 'plant__name']
    date_hierarchy = 'from_date'


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['cargo_name', 'plant', 'simulation', 'delivery_date', 'amount']
    list_filter = ['simulation', 'plant', 'delivery_date']
    search_fields = ['cargo_name', 'simulation__name', 'plant__name']
    date_hierarchy = 'delivery_date'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'plant', 'simulation', 'daily_demand', 'from_date', 'to_date']
    list_filter = ['simulation', 'plant', 'created_at']
    search_fields = ['name', 'simulation__name', 'plant__name']
    date_hierarchy = 'from_date'


@admin.register(APIConfiguration)
class APIConfigurationAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'api_url', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'api_url', 'user__username']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'api_url')
        }),
        ('Supplier Mapping', {
            'fields': (
                'supplier_table',
                'supplier_name_col',
                'supplier_daily_supply_col',
                'supplier_from_date_col',
                'supplier_to_date_col'
            )
        }),
        ('Cargo Mapping', {
            'fields': (
                'cargo_table',
                'cargo_name_col',
                'cargo_date_col',
                'cargo_amount_col'
            )
        }),
        ('Customer Mapping', {
            'fields': (
                'customer_table',
                'customer_name_col',
                'customer_daily_demand_col',
                'customer_from_date_col',
                'customer_to_date_col'
            )
        }),
    )