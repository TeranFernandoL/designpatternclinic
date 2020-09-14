from django import forms
import warnings
from .models import *
from django.contrib.auth import authenticate, get_user_model


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': u'Please enter a correct %(username)s and password.Note that both fields may be case-sensitive.',
        'inactive': u'This account is inactive',
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        UserModel = get_user_model()

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None or self.user_cache.type != 'PACIENTE':
                self.add_error(None,
                               'Por favor, introduzca usuario y password correctos.')
            elif not self.user_cache.is_active:
                self.add_error('username',
                               'Usuario inactivo.')
        return self.cleaned_data

    def check_for_test_cookie(self):
        warnings.warn("check_for_test_cookie is deprecated; ensure your login "
                      "view is CSRF-protected.", DeprecationWarning)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class AuthenticationMedicoForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': u'Please enter a correct %(username)s and password.Note that both fields may be case-sensitive.',
        'inactive': u'This account is inactive',
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationMedicoForm, self).__init__(*args, **kwargs)
        UserModel = get_user_model()

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            print(self.user_cache.type)
            if self.user_cache is None or self.user_cache.type != 'MEDICO':
                self.add_error(None,
                               'Por favor, introduzca usuario y password correctos.')
            elif not self.user_cache.is_active:
                self.add_error('username',
                               'Usuario inactivo.')
        return self.cleaned_data

    def check_for_test_cookie(self):
        warnings.warn("check_for_test_cookie is deprecated; ensure your login "
                      "view is CSRF-protected.", DeprecationWarning)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class RegistroUsuarioForm(forms.ModelForm):
    nombre = forms.CharField(required=True)
    apellido = forms.CharField(required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password', 'nombre', 'apellido', 'cedula', 'direccion', 'telefono')

    def clean_password(self):
        if len(self.cleaned_data.get('password')) < 6:
            self.add_error('password', 'Mínimo 6 caracteres.')
        else:
            return self.cleaned_data.get('password')

    def clean_email(self):
        if Usuario.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', 'El email ya ha sido registrado.')
        else:
            return self.cleaned_data['email']

    def clean_username(self):
        if Usuario.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', 'El usuario ya ha sido registrado.')
        else:
            return self.cleaned_data['username']

    def save(self, commit=True):
        user = Usuario.objects.create(
            email=self.cleaned_data.get('email'),
            username=self.cleaned_data.get('username'),
            nombre=self.cleaned_data.get('nombre'),
            apellido=self.cleaned_data.get('apellido'),
            cedula=self.cleaned_data.get('cedula'),
            direccion=self.cleaned_data.get('direccion'),
            telefono=self.cleaned_data.get('telefono'),
            type='PACIENTE'
        )
        Paciente.objects.create(usuario=user)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user


class RegistroMedicoForm(forms.ModelForm):
    nombre = forms.CharField(required=True)
    apellido = forms.CharField(required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password', 'nombre', 'apellido', 'cedula', 'direccion', 'telefono')

    def clean_password(self):
        if len(self.cleaned_data.get('password')) < 6:
            self.add_error('password', 'Mínimo 6 caracteres.')
        else:
            return self.cleaned_data.get('password')

    def clean_email(self):
        if Usuario.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error('email', 'El email ya ha sido registrado.')
        else:
            return self.cleaned_data['email']

    def clean_username(self):
        if Usuario.objects.filter(username=self.cleaned_data['username']).exists():
            self.add_error('username', 'El usuario ya ha sido registrado.')
        else:
            return self.cleaned_data['username']

    def save(self, commit=True):
        user = Usuario.objects.create(
            email=self.cleaned_data.get('email'),
            username=self.cleaned_data.get('username'),
            nombre=self.cleaned_data.get('nombre'),
            apellido=self.cleaned_data.get('apellido'),
            cedula=self.cleaned_data.get('cedula'),
            direccion=self.cleaned_data.get('direccion'),
            telefono=self.cleaned_data.get('telefono'),
            type='MEDICO'
        )
        Medico.objects.create(usuario=user)
        user.set_password(self.cleaned_data.get('password'))
        user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'cedula', 'direccion', 'telefono', 'type')

    def clean_nombre(self):
        if len(self.cleaned_data.get('nombre')) > 0:
            return self.cleaned_data.get('nombre').lower()
        else:
            self.add_error('nombre', 'Ingrese un nombre válido.')

    def clean_apellido(self):
        if len(self.cleaned_data.get('apellido')) > 0:
            return self.cleaned_data.get('apellido').lower()
        else:
            self.add_error('apellido', 'Ingrese un apellido válido.')

    def clean_telefono(self):
        lon = len(self.cleaned_data.get('telefono'))
        if (lon > 0 and lon < 7):
            self.add_error('telefono', 'Ingrese un número válido.')
        else:
            return self.cleaned_data.get('telefono')


class UpdateCitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ('diagnostico',)


class RegistroCitaForm(forms.ModelForm):
    medico = forms.ModelChoiceField(queryset=Medico.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    fecha = forms.DateField(required=False)

    class Meta:
        model = Cita
        fields = ['medico', 'fecha', 'motivo']

    def save(self, commit=True, user=None):
        cita = Cita.objects.create(medico=self.cleaned_data.get('medico'), fecha=self.cleaned_data.get('fecha'),
                                   motivo=self.cleaned_data.get('motivo'), estado='REGISTRADO')
        medicamento = Medicamento()
        cita.attach(medicamento)
        cita.some_business_logic()
        return cita
