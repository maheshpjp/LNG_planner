# Generated migration to move quantity fields to date range models

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('lng_planner', '0006_remove_supplierschedule_supplier_and_more'),
    ]

    operations = [
        # Remove daily_supply from Supplier, add to SupplierDate
        migrations.AddField(
            model_name='supplierdate',
            name='daily_supply',
            field=models.FloatField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
                help_text='MT per day'
            ),
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='daily_supply',
        ),
        # Remove daily_demand from Customer, add to CustomerDate
        migrations.AddField(
            model_name='customerdate',
            name='daily_demand',
            field=models.FloatField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
                help_text='MT per day'
            ),
        ),
        migrations.RemoveField(
            model_name='customer',
            name='daily_demand',
        ),
        # Remove daily_refinery_supply from Refinery, add to RefineryDate
        migrations.AddField(
            model_name='refinerydate',
            name='daily_refinery_supply',
            field=models.FloatField(
                default=0,
                validators=[django.core.validators.MinValueValidator(0)],
                help_text='MT per day'
            ),
        ),
        migrations.RemoveField(
            model_name='refinery',
            name='daily_refinery_supply',
        ),
    ]
