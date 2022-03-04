from django.contrib import admin
from django.urls import path
from buscas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.busca, name='busca'),
    path('resultado', views.busca, name='busca'),

]
