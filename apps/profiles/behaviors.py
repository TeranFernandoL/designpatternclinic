from django.db import models
from django.conf import settings


class Person(models.Model):
    nombre = models.CharField(blank=True, null=True, max_length=50)
    apellido = models.CharField(blank=True, null=True, max_length=50)
    cedula = models.CharField(blank=True, null=True, max_length=50)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True, max_length=50)
    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True