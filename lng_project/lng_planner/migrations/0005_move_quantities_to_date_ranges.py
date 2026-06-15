from django.db import migrations, models
import django.core.validators


def copy_parent_amounts_to_date_ranges(apps, schema_editor):
    SupplierDate = apps.get_model("lng_planner", "SupplierDate")
    CustomerDate = apps.get_model("lng_planner", "CustomerDate")
    RefineryDate = apps.get_model("lng_planner", "RefineryDate")

    for supplier_date in SupplierDate.objects.select_related("supplier"):
        supplier_date.daily_supply = supplier_date.supplier.daily_supply
        supplier_date.save(update_fields=["daily_supply"])

    for customer_date in CustomerDate.objects.select_related("customer"):
        customer_date.daily_demand = customer_date.customer.daily_demand
        customer_date.save(update_fields=["daily_demand"])

    for refinery_date in RefineryDate.objects.select_related("refinery"):
        refinery_date.daily_refinery_supply = refinery_date.refinery.daily_refinery_supply
        refinery_date.save(update_fields=["daily_refinery_supply"])


class Migration(migrations.Migration):

    dependencies = [
        ("lng_planner", "0004_remove_customer_from_date_remove_customer_to_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="supplierdate",
            name="daily_supply",
            field=models.FloatField(
                default=0,
                help_text="MT per day",
                validators=[django.core.validators.MinValueValidator(0)],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="customerdate",
            name="daily_demand",
            field=models.FloatField(
                default=0,
                help_text="MT per day",
                validators=[django.core.validators.MinValueValidator(0)],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="refinerydate",
            name="daily_refinery_supply",
            field=models.FloatField(
                default=0,
                help_text="MT per day",
                validators=[django.core.validators.MinValueValidator(0)],
            ),
            preserve_default=False,
        ),
        migrations.RunPython(copy_parent_amounts_to_date_ranges, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="supplier",
            name="daily_supply",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="daily_demand",
        ),
        migrations.RemoveField(
            model_name="refinery",
            name="daily_refinery_supply",
        ),
    ]
