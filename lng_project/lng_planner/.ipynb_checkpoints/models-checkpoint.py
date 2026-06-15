from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Plant(models.Model):
    """Plants/Terminals where LNG is stored"""
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Simulation(models.Model):
    """Stores simulation configurations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='simulations', null=True, blank=True)
    name = models.CharField(max_length=200, default='Untitled Simulation')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_master = models.BooleanField(default=False, help_text="Master simulation loaded from SAP")
    sap_api_url = models.URLField(blank=True, help_text="SAP API URL for refreshing master data")
    last_sap_sync = models.DateTimeField(null=True, blank=True, help_text="Last time master data was synced from SAP")

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{'[MASTER] ' if self.is_master else ''}{self.name} - {self.start_date} to {self.end_date}"


class PlantInventory(models.Model):
    """Opening inventory for each plant in a simulation"""
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='plant_inventories')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    opening_inventory = models.FloatField(validators=[MinValueValidator(0)], help_text="MT")

    class Meta:
        unique_together = ['simulation', 'plant']
        ordering = ['plant__name']

    def __str__(self):
        return f"{self.plant.name} - {self.opening_inventory} MT"


class Supplier(models.Model):
    """Suppliers with daily supply rates"""
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='suppliers')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='suppliers')
    name = models.CharField(max_length=200)
    daily_supply = models.FloatField(validators=[MinValueValidator(0)], help_text="MT per day")
    from_date = models.DateField()
    to_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['plant__name', 'name']

    def __str__(self):
        return f"{self.name} → {self.plant.name} - {self.daily_supply} MT/day"


class Cargo(models.Model):
    """One-time cargo deliveries"""
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='cargos')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='cargos')
    cargo_name = models.CharField(max_length=200)
    delivery_date = models.DateField()
    amount = models.FloatField(validators=[MinValueValidator(0)], help_text="MT")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['delivery_date', 'plant__name', 'cargo_name']

    def __str__(self):
        return f"{self.cargo_name} → {self.plant.name} - {self.amount} MT on {self.delivery_date}"


class Customer(models.Model):
    """Customers with daily demand"""
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE, related_name='customers')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=200)
    daily_demand = models.FloatField(validators=[MinValueValidator(0)], help_text="MT per day")
    from_date = models.DateField()
    to_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['plant__name', 'name']

    def __str__(self):
        return f"{self.name} ← {self.plant.name} - {self.daily_demand} MT/day"


class APIConfiguration(models.Model):
    """Store API configurations for data import"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_configs')
    name = models.CharField(max_length=200)
    api_url = models.URLField()
    
    # Supplier mapping
    supplier_table = models.CharField(max_length=100, default='suppliers')
    supplier_name_col = models.CharField(max_length=100)
    supplier_daily_supply_col = models.CharField(max_length=100)
    supplier_from_date_col = models.CharField(max_length=100)
    supplier_to_date_col = models.CharField(max_length=100)
    
    # Cargo mapping
    cargo_table = models.CharField(max_length=100, default='cargos')
    cargo_name_col = models.CharField(max_length=100)
    cargo_date_col = models.CharField(max_length=100)
    cargo_amount_col = models.CharField(max_length=100)
    
    # Customer mapping
    customer_table = models.CharField(max_length=100, default='customers')
    customer_name_col = models.CharField(max_length=100)
    customer_daily_demand_col = models.CharField(max_length=100)
    customer_from_date_col = models.CharField(max_length=100)
    customer_to_date_col = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name