from django.contrib import admin
from django.urls import path
from buscas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('layout-static.html', views.layout, name='layout'),
    path('resultado', views.busca, name='busca'),

]
