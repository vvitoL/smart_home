from django.db import models


class Device(models.Model):  # eq Film
    name = models.CharField(max_length=32)
    desc = models.TextField(max_length=256)
    state = models.BooleanField(default=False)
