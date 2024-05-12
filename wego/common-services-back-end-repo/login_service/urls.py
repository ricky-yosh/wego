from django.urls import include, path
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('create-account/', views.create_Account, name='create_account'),
    path('verify-account/', views.verify_Account, name='verify_account'),
    path('', views.get_routes),
    path('token/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # do we need to add common-services/ prefix?
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'), # do we need to add common-services/ prefix?
]