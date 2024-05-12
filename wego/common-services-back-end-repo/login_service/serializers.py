from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    @csrf_exempt
    def get_token(cls, user):
        token = super().get_token(user)
        token['cloud'] = settings.CLOUD_TYPE
        token['username'] = user.username
        return token