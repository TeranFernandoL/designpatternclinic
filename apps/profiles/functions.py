from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import *
from django.core.mail.message import EmailMessage
from .patterns.observer import Observer

class SendEmail(Observer):
    def update(self, subject):
        subject_user, from_email = 'Ahorro confirmado ', ' Clinica Velazco <email>'
        destiny = "luis.teran@unmsm.edu.pe"
        mensajito = 'Estimado usuario, te confirmamos que el monto ahorrado es de. Gracias por su preferencia. Cordialmente,Cash Box.'
        message_user = EmailMessage(subject_user, mensajito, from_email, [destiny])
        message_user.send(fail_silently=True)
        print("correo enviado a {} {}".format(subject.nombre_paciente(),subject.apellido_paciente()))
        pass