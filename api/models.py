from django.db import models
from django.utils.translation import gettext_lazy as _


class ExtraInfo(models.Model):

    class DeviceKinds(models.TextChoices):
        UNKNOWN = "UN", _("Unknown")
        BULB = "BU", _("Bulb")
        RELAY = "RE", _("Relay")
        GATE = "GA", _("Gate")
        BLIND = "BL", _("Blind")
        TUYA = "TU", _("Tuya Device")

    consumption = models.IntegerField()
    device_kind = models.CharField(
        max_length=2,
        choices=DeviceKinds.choices,
        default=DeviceKinds.UNKNOWN,
    )

    def __str__(self):
        return f"Kind: {self.device_kind} - Consumption: {self.consumption} [W]"


class Device(models.Model):  # eq Film
    name = models.CharField(max_length=32)
    desc = models.TextField(max_length=256)
    state = models.BooleanField(default=False)
    last_mod = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    amount_changes = models.IntegerField()
    plc_register = models.IntegerField(null=True, blank=True)
    modbus_register = models.IntegerField(null=True, blank=True)

    extra_info = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.long_name

    @property
    def long_name(self):
        return f"{self.name} - ({self.desc}) - ({self.created})"


class Sensor(models.Model):
    name = models.CharField(max_length=32)
    desc = models.TextField(max_length=256)
    act_temp = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SensorHistory(models.Model):
    temperature = models.FloatField(blank=True,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='histories')

    def __str__(self):
        return f"({self.temperature})*C - {self.sensor.name} - {self.created.date()} - {self.created.time()}"


class Owner(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    devices = models.ManyToManyField(Device)
    sensors = models.ManyToManyField(Sensor)

    def __str__(self):
        return self.name or ''
