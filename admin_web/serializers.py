from rest_framework.serializers import ModelSerializer
from .models import user, client


class UserSerializer(ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'


class ClientSerializer(ModelSerializer):
    class Meta:
        model = client
        fields = '__all__'
