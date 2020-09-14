from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import *
from django.core.mail.message import EmailMessage
from .patterns.observer import Observer
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

class SendEmail(Observer):
    def update(self, subject):
        subject_user, from_email = 'Cita Registrada ', ' Clinica Observer <email>'
        mensajito = 'Estimado le confirmamos que su cita ha sido registrada gracias por confiar en la clinica Observer.'
        message_user = EmailMessage(subject_user, mensajito, "hagisolomon2@gmail.com", ["hagisolomon2@gmail.com"])
        message_user.send(fail_silently=True)
        print("correo enviado")
        pass

class ExportPDF():
    def some_view(request):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, "Hello world.")
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')