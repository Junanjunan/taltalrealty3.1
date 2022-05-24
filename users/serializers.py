from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model= models.User
        fields = ('__all__')