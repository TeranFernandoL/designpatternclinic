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


class Especialidad(models.Model):
    nombre = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Paciente, self).save()
        context = Context(Cita())
        context.do_some_business_logic()
        return None

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'


class Cita(models.Model, Subject, Strategy):
    class State(Enum):
        REGISTRADO = 'REGISTRADO'
        CANCELED = 'CANCELED'
        TERMINADO = 'TERMINADO'

    _state: int = None

    _observers: List[Observer] = []

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=True, null=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(blank=True, null=True, max_length=200,
                              choices=[(item.name, item.value) for item in State])
    diagnostico = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.id)

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        self._state = datetime.datetime.now().hour
        self.notify()

    def do_algorithm(self, data):
        return "aqui no ha pasado nada "

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'


class Medicamento(models.Model, Observer):
    class MedicamentoBasico(Component):
        def operation(self):
            return None

    class MedicamentoInyectable(Decorator):
        def operation(self):
            return self.component.operation()

    class MedicamentoCovid(Decorator):
        def operation(self):
            return self.component.operation()

    nombre = models.CharField(blank=False, max_length=50)
    presentacion = models.CharField(blank=False, max_length=50)
    volumen = models.CharField(blank=False, max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return ('%s - %s') % (self.nombre, self.presentacion)

    def client_code(self, component):
        component.operation()
        return None

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Medicamento, self).save()
        simple = self.MedicamentoBasico()
        self.client_code(simple)
        decorator1 = self.MedicamentoInyectable(simple)
        self.client_code(decorator1)
        return None

    def update(self, subject: Subject) -> None:
        print("por favoorrrr :´v ")
        self.nombre = 'vicvaporum'
        self.presentacion = "hola soy german"
        self.volumen = "gaaa"
        self.descripcion = "miau"
        self.save(force_insert=True)

    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'


class Consulta(models.Model, Strategy):
    paciente = models.ForeignKey(Paciente, blank=True, null=True, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, blank=True, null=True)
    diagnostico = models.TextField(blank=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ('%s - %s') % (self.paciente, self.medico)

    def do_algorithm(self, data):
        print("un ga y a seguir con esta webada")
        return "que chucha fue "

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'


class Tratamiento(models.Model):
    consulta = models.ForeignKey(Consulta, blank=True, null=True, on_delete=models.CASCADE)
    medicamento = models.ManyToManyField(Medicamento, blank=True)
    descripcion = models.TextField(blank=False)

    def __str__(self):
        return ('%s - %s') % (self.consulta, self.medicamento)

    class Meta:
        verbose_name = 'Tratamiento'
        verbose_name_plural = 'Tratamientos'


class Consultorio(SingletonModel):
    nombre = models.CharField(blank=False, max_length=50)
    direccion = models.TextField(blank=False)
    mision = models.TextField(blank=False)
    vision = models.TextField(blank=False)
    eslogan = models.CharField(blank=False, max_length=150)
    telefono = models.CharField(blank=False, max_length=50)
    correo = models.EmailField(blank=False)
    foto = models.ImageField(upload_to='home')
