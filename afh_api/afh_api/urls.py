"""
URL configuration for afh_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),#endpoints de autenticacion
    path('reset/', include('passwordresetcode.urls')),#endpoints de reset el codigo de autenticacion
    path('tool/', include('tool.urls')),#endpoints de las herramientas
    path('ticket/', include('ticket.urls')), #enpoints de los tickets
    path('customer/', include('Customer.urls')), #endpoints de los clientes
    path('item/', include('item.urls')), #endpoints de los items
    path('option/', include('Option.urls')), #endpoints de las opciones
    path('quote/', include('Quotes.urls')), #endpoints de las cotizaciones
]

