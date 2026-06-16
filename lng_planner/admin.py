from django.contrib import admin
from .models import (
    Simulation, Supplier, Cargo, Customer, Plant, PlantInventory, APIConfiguration,
    SupplierDate, CustomerDate, Refinery, RefineryDate, SimulationComment
)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'created_at']
    search_fields = ['name', 'location']


class PlantInventoryInline(admin.TabularInline):
    model = PlantInventory
    extra = 1
    fields = ['plant', 'opening_inventory']


class SupplierDateInline(admin.TabularInline):
    model = SupplierDate
    extra = 1
    fields = ['from_date', 'to_date', 'daily_supply']


class SupplierInline(admin.TabularInline):
    model = Supplier
    extra = 1
    fields = ['name', 'plant']


class CustomerDateInline(admin.TabularInline):
    model = CustomerDate
    extra = 1
    fields = ['from_date', 'to_date', 'daily_demand']


class CargoInline(admin.TabularInline):
    model = Cargo
    extra = 1
    fields = ['cargo_name', 'plant', 'delivery_date', 'amount']


class CustomerInline(admin.TabularInline):
    model = Customer
    extra = 1
    fields = ['name', 'plant']


class RefineryDateInline(admin.TabularInline):
    model = RefineryDate
    extra = 1
    fields = ['from_date', 'to_date', 'daily_refinery_supply']


class RefineryInline(admin.TabularInline):
    model = Refinery
    extra = 1
    fields = ['name', 'plant', 'daily_refinery_supply']


class SimulationCommentInline(admin.TabularInline):
    model = SimulationComment
    extra = 0
    fields = ['comment', 'created_by', 'created_at']
    readonly_fields = ['created_by', 'created_at']


@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'start_date', 'end_date', 'is_master', 'is_active', 'last_sap_sync', 'updated_at']
    list_filter = ['is_active', 'is_master', 'created_at', 'user']
    search_fields = ['name', 'user__username']
    date_hierarchy = 'created_at'
    inlines = [PlantInventoryInline, SupplierInline, CustomerInline, CargoInline, RefineryInline, SimulationCommentInline]
    
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
    list_display = ['name', 'plant', 'simulation']
    list_filter = ['simulation', 'plant', 'created_at']
    search_fields = ['name', 'simulation__name', 'plant__name']
    date_hierarchy = 'created_at'
    inlines = [SupplierDateInline]


@admin.register(SupplierDate)
class SupplierDateAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'from_date', 'to_date', 'daily_supply']
    list_filter = ['from_date', 'to_date']
    search_fields = ['supplier__name']
    date_hierarchy = 'from_date'


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['cargo_name', 'plant', 'simulation', 'delivery_date', 'amount']
    list_filter = ['simulation', 'plant', 'delivery_date']
    search_fields = ['cargo_name', 'simulation__name', 'plant__name']
    date_hierarchy = 'delivery_date'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'plant', 'simulation']
    list_filter = ['simulation', 'plant', 'created_at']
    search_fields = ['name', 'simulation__name', 'plant__name']
    date_hierarchy = 'created_at'
    inlines = [CustomerDateInline]


@admin.register(CustomerDate)
class CustomerDateAdmin(admin.ModelAdmin):
    list_display = ['customer', 'from_date', 'to_date', 'daily_demand']
    list_filter = ['from_date', 'to_date']
    search_fields = ['customer__name']
    date_hierarchy = 'from_date'


@admin.register(Refinery)
class RefineryAdmin(admin.ModelAdmin):
    list_display = ['name', 'plant', 'simulation']
    list_filter = ['simulation', 'plant', 'created_at']
    search_fields = ['name', 'simulation__name', 'plant__name']
    date_hierarchy = 'created_at'
    inlines = [RefineryDateInline]


@admin.register(RefineryDate)
class RefineryDateAdmin(admin.ModelAdmin):
    list_display = ['refinery', 'from_date', 'to_date', 'daily_refinery_supply']
    list_filter = ['from_date', 'to_date']
    search_fields = ['refinery__name']
    date_hierarchy = 'from_date'


@admin.register(SimulationComment)
class SimulationCommentAdmin(admin.ModelAdmin):
    list_display = ['simulation', 'created_by', 'created_at']
    list_filter = ['created_at', 'created_by']
    search_fields = ['simulation__name', 'comment']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'created_by']


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