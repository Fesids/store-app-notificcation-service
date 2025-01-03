from django.urls import path, include

from infraestructure.notifications.views import Teste

urlpatterns = [
    path('/teste', Teste.as_view(), name="teste")
]