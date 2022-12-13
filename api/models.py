import datetime

from django.utils import timezone
from django.db import models


class ExtraInfo(models.Model):

    kinds = {
        (0, "Unknown"),
        (1, "Bulb"),
        (2, "Relay"),
        (3, "Gate"),
        (4, "Blind")
    }

    consumption = models.IntegerField()
    kind = models.IntegerField(choices=kinds, default=0)

    def __str__(self):
        return self.kind + self.consumption


class Device(models.Model):  # eq Film
    name = models.CharField(max_length=32)
    desc = models.TextField(max_length=256)
    state = models.BooleanField(default=False)
    last_mod = models.DateTimeField(null=True, blank=True)
    created = models.DateField(default=timezone.now)
    amount_changes = models.IntegerField()

    extra_info = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.long_name

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
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='history')

    def __str__(self):
        return F"{self.sensor.name} - {self.temperature}*C - {self.created}"
