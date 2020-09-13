from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import *


def Logear(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('clinico:dashboard')
    else:
        login_form = LoginForm(request.POST)
        mensaje = "Los datos ingresados no son validos"
        return render(request, 'clinico/login.html', {'login_form': login_form, 'mensaje': mensaje})

def LogearMedico(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('clinico:dashboard_medico')
    else:
        login_form = LoginForm(request.POST)
        mensaje = "Los datos ingresados no son validos"
        return render(request, 'clinico/login.html', {'login_form': login_form, 'mensaje': mensaje})