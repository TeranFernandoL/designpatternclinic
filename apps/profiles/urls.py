from django.urls import path
from apps.profiles.views import *

app_name = "clinico"
urlpatterns = [
    path('registro/', UserRegisterView.as_view(), name='registro'),
    path('registromedico/', MedicoRegisterView.as_view(), name='registro_medico'),
    path('login/', LogIn.as_view(), name='login'),
    path('loginmedico/', LogInMedico.as_view(), name='login_medico'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('salir/', LogoutView.as_view(), name='logout'),
    path('paciente/', Dashboard.as_view(), name='dashboard'),
    path('medico/', DashboardMedico.as_view(), name='dashboard_medico'),
    # path('pacientes/cita/', SolicitudCita.as_view(), name='cita'),
    path('cancelarcita/<int:pk>', CancelCitaView.as_view(), name='cancel_cita'),
    path('diagnosticocita/<int:pk>', UpdateCitaView.as_view(), name='update_cita'),
    path('miscitasmedico/', ListCitasMedicoView.as_view(), name='mis_citas_medicos'),
    path('miscitasmedicoregistradas/', ListCitasDiagnosticarView.as_view(), name='mis_citas_medicos_register'),
    path('miscitasmedicocompletadas/', ListCitasDiagnosticadasView.as_view(), name='mis_citas_medicos_completed'),
    path('registrar/cita/', CrearCita.as_view(), name='crear_cita'),
    path('miscitas/', ListCitasView.as_view(), name='mis_citas'),
    path('miscitascanceladas/', ListCitasPacienteCanceledView.as_view(), name='mis_citas_canceled'),
    path('miscitasregistradas/', ListCitasPacienteRegistradaView.as_view(), name='mis_citas_registrada'),
    path('miscitasterminadas/', ListCitasPacienteCompletedView.as_view(), name='mis_citas_completada'),
    path('detailcita/<int:pk>', CitaProfileView.as_view(), name='mis_citas_detail'),
    path('export/<int:pk>', DownloadPaciente.as_view(), name='export'),

]
