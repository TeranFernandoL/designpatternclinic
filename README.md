CONFIGURACIONES 
===============
Se debe tener instalado en el proyecto :

- PYTHON 3.7 
- POSTGRESQL 
- VIRTUALENV 


1.- Clonar el Proyecto 

git clone https://github.com/TeranFernandoL/designpatternclinic.git

2.- De preferencia usar virtualenv para crear un entorno y instalar las librerias 

virtualenv -p python3 "nombre_virtualenv"

3.- Con el virtualenv activado situarse en el proyecto y instalar las librerias 

pip install -r requirements.txt

4.- Una vez instaladas las librerias entrar a POSTGRES y crear la base de datos 

CREATE DATABASE "Nombre_Database"

5.- Una vez creada la base de datos entrar a la raiz ..config/settings/local.py y setear los valores de tu BD

DATABASES = {

    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': "NOMBRE_DATABASE",
        'USER': "USUARIO_POSTGRES",
        'PASSWORD': "PASSWORD_POSTGRES",
        'HOST': 'localhost',
        'PORT': '',
    }
}

6.- Una vez seteados los valores de la Base de datos pasamos a ejecutar el proyecto nos situamos dentro del directorio dessignpatterns/ y ejecutamos el comando para hacer migraciones en la base de datos

```
python manage.py migrate --settings='config.settings.local'
```

7.- Luego de crear las migraciones creamos un usuario administrador nos pedira valores como usuario, email y password llenamos y listo

```
python manage.py createsuperuser --settings='config.settings.local'
```

8.-  Por ultimo corremos el proyecto

```
python manage.py runserver 8000 --settings='config.settings.local'
```