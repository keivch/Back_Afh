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
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AFH API",
        default_version='v1',
        description="API para gestionar las funcionalidades de la aplicación",
        terms_of_service="https://www.tusitio.com/terminos/",
        contact=openapi.Contact(email="juanchopolla@tusitio.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

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
    path('workorder/', include('WorkOrder.urls')), #endpoints de las ordenes de trabajo
    path('deliverycertificate/', include('Delivery_certificate.Urls')), #endpoints de los certificados de entrega
    path('exhibit/', include('exhibit.Urls')), #endpoints de los exhibits
    path('egress/', include('Financial_movement.urls_egress')),#enpoints de los egress
    path('income/', include('Financial_movement.urls_income')),
    path('balans/', include('Financial_movement.urls_balans')),
    path('workadvance/', include('WorkAdvance.urls')), #endpoints de los avances de trabajo
    path('workprogress/', include('WorkProgress.urls')), #endpoints de los progresos de trabajo

    #rutas de la documentacion
    # rutas para swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

