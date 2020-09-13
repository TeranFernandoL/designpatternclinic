from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.contrib import auth
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from django.views.generic import CreateView, View, UpdateView, ListView
from class_based_auth_views.views import LoginView
from .models import *
from .functions import *
from .forms import *
from django.contrib import messages
from django.views.generic.edit import ModelFormMixin
from django.urls import reverse_lazy
from .patterns.observer import Subject, Observer


class UserRegisterView(AnonymousRequiredMixin, CreateView):
    template_name = 'clinico/registro.html'
    model = Usuario
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('clinico:dashboard')

    def form_valid(self, form):
        self.object = form.save()
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object)
        return super(ModelFormMixin, self).form_valid(form)


class MedicoRegisterView(AnonymousRequiredMixin, CreateView):
    template_name = 'doctores/registro.html'
    model = Usuario
    form_class = RegistroMedicoForm
    success_url = reverse_lazy('clinico:dashboard')

    def form_valid(self, form):
        self.object = form.save()
        self.object.backend = 'django.contrib.auth.backends.ModelBackend'
        login(self.request, self.object)
        return super(ModelFormMixin, self).form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'clinico/profile.html'
    context_object_name = 'user'
    form_class = UpdateUserForm
    success_url = reverse_lazy('clinico:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if self.request.user.type == 'PACIENTE':
            context['paciente'] = Paciente.objects.get(usuario=self.request.user)
        if self.request.user.type == 'MEDICO':
            context['medico'] = Medico.objects.get(usuario=self.request.user)
        return context

    def form_valid(self, form):
        self.object = form.save()
        messages.add_message(self.request, messages.SUCCESS, 'Informacion editada.')
        return super(ModelFormMixin, self).form_valid(form)


class Dashboard(LoginRequiredMixin, TemplateView):
    login_url = 'clinico:login'
    template_name = 'pacientes/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        return context


class DashboardMedico(LoginRequiredMixin, TemplateView):
    login_url = 'doctores:login'
    template_name = 'doctores/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardMedico, self).get_context_data(**kwargs)
        return context


class LogIn(AnonymousRequiredMixin, LoginView):
    template_name = 'clinico/login.html'
    form_class = AuthenticationForm
    authenticated_redirect_url = reverse_lazy('clinico:dashboard')

    def get_success_url(self):
        return reverse_lazy('clinico:dashboard')


class LogInMedico(AnonymousRequiredMixin, LoginView):
    template_name = 'doctores/login.html'
    form_class = AuthenticationMedicoForm
    authenticated_redirect_url = reverse_lazy('clinico:dashboard_medico')

    def get_success_url(self):
        return reverse_lazy('clinico:dashboard_medico')


class LogoutView(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            auth.logout(self.request)
        return redirect(reverse_lazy('home:home'))


class SolicitudCita(TemplateView):
    template_name = 'pacientes/cita.html'

    def get_context_data(self, **kwargs):
        context = super(SolicitudCita, self).get_context_data(**kwargs)
        context['paciente'] = Paciente.objects.get(usuario=self.request.user.id)
        return context


class CrearCita(LoginRequiredMixin, CreateView):
    template_name = 'pacientes/crearcita.html'
    model = Cita
    form_class = RegistroCitaForm

    def form_valid(self, form):
        self.object = form.save(commit=True)
        paciente = self.request.user.paciente
        cita = Cita.objects.get(id=self.object.id)
        cita.paciente = paciente
        cita.save()
        messages.add_message(self.request, messages.SUCCESS, 'Gracias por añadir a este mongol.')
        return super(ModelFormMixin, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('clinico:dashboard')


class ListCitasView(ListView, LoginRequiredMixin):
    template_name = 'pacientes/miscitas.html'
    context_object_name = 'citas'
    model = Cita

    def get_queryset(self):
        return Cita.objects.filter(paciente=self.request.user.paciente).order_by('id')
