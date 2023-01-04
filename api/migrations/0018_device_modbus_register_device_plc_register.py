# Generated by Django 4.1.4 on 2022-12-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0017_remove_device_modbus_register_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="device",
            name="modbus_register",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="device",
            name="plc_register",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]