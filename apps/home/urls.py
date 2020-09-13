from django.urls import path
from apps.home.views import *

app_name = "home"
urlpatterns = [
    path('', Home.as_view(), name='home'),
]