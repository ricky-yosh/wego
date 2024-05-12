"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    path('demand-services/plugin99/', include('plugin99.urls')),
    path('new/path/', include('plugin99.urls')),
    path('new/path/', include('plugin99.urls'))

    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Pastebin API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@xyz.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)
urlpatterns = [
    path('demand-services/construction-wizard/', include('construction_wizard.urls')),
    path('demand-services/lifetime-drones/', include('lifetime_drones.urls')),

    path('customer-services/', include('customer_manager.urls')),
    #path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
