from __future__ import annotations
from django.db import models
import six
# imports necesarios para crear un Custom User Manager
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .behaviors import *
from .patterns.observer import Observer, Subject
from .patterns.strategy import *
from .patterns.decorator import *
from .patterns.singleton import *
from .patterns.factory import *
from abc import ABC, abstractmethod
from random import randrange
from typing import List
from enum import Enum
import datetime


class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, username, email, password, is_staff,
                     is_superuser, **extra_fields):
        email = self.normalize_email(email)
        if not email:
            raise ValueError('El email debe ser obligatorio')
        user = self.model(username=username, email=email, is_active=True,
                          is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False,
                                 False, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True,
                                 True, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin, Person):
    class Type(Enum):
        PACIENTE = 'PACIENTE'
        MEDICO = 'MEDICO'
        ADMINISTRADOR = 'ADMINISTRADOR'

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=200, blank=True, null=True, choices=[(item.name, item.value) for item in Type])
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_short_name(self):
        return self.username


class Medico(TimeStampedModel):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    especialidad = models.CharField(blank=True, null=True, max_length=200)
    cedula = models.CharField(blank=True, null=True, max_length=200)
    foto = models.FileField(upload_to='medicos', blank=True, null=True)

    def __str__(self):
        return "{}-{}".format(self.usuario.nombre, self.usuario.apellido)

    class Meta:
        verbose_name = 'Medico'
        verbose_name_plural = 'Medico'


class Paciente(TimeStampedModel):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    descripcion = models.CharField(blank=True, null=True, max_length=200)
    foto = models.FileField(upload_to='pacientes', blank=True, null=True)

    def __str__(self):
        return "{}-{}".format(self.usuario.nombre, self.usuario.apellido)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'


class Cita(models.Model, Subject):
    class CitaNormal(Strategy):
        def do_algorithm(self, data):
            pass

    class CitaEmergencia(Strategy):
        def do_algorithm(self, data):
            data.sala = "la sala esta ocupada por el paciente de esta cita"
            data.save()
            pass

    class CitaDomicilio(Strategy):
        def do_algorithm(self, data):
            data.domicilio = True
            data.save()
            pass

    class State(Enum):
        REGISTRADO = 'REGISTRADO'
        CANCELED = 'CANCELED'
        TERMINADO = 'TERMINADO'

    NORMAL = 'NORMAL'
    EMERGENCIA = 'EMERGENCIA'
    DOMICILIO = 'DOMICILIO'

    _observers: List[Observer] = []

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=True, null=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(blank=True, null=True, max_length=200,
                              choices=[(item.name, item.value) for item in State])
    type = models.CharField(blank=True, null=True, max_length=200, choices=(
        (NORMAL, "NORMAL"), (EMERGENCIA, "EMERGENCIA"), (DOMICILIO, "DOMICILIO")
    ))
    sala = models.CharField(max_length=200, blank=True, null=True)
    domicilio = models.BooleanField(default=False)
    diagnostico = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.id)

    # Patron Observer
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        self.notify()

    # Final del Patron Observer
    def nombre_paciente(self):
        usuario = self.paciente.usuario
        return usuario.nombre

    def apellido_paciente(self):
        usuario = self.paciente.usuario
        return usuario.apellido

    def direccion_paciente(self):
        usuario = self.paciente.usuario
        return usuario.direccion

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'






