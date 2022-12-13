from django.contrib import admin

from api.models import Device, ExtraInfo, Sensor, SensorHistory

admin.site.register(Device)
admin.site.register(ExtraInfo)
admin.site.register(Sensor)
admin.site.register(SensorHistory)
