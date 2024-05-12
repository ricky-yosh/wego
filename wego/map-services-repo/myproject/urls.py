# myproject/urls.py

# from django.contrib import admin
from django.urls import path, include # type: ignore
from rest_framework import permissions # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore

schema_view = get_schema_view(
    openapi.Info(
        title="Map Services",
        default_version='v6.0.0',
        description="API documentation for Map Services",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # path('admin/', admin.site.urls), Not using admin, useful for managing data, but we will not need it
    path('map-services/map-api/', include('map_services.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
