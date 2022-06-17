from rest_framework import serializers
from users import models as users_models
from books import models as books_models
from contracts import models as contracts_models
from managements import models as managements_models
import jwt
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):

    password =serializers.CharField(write_only=True)

    class Meta:
        model = users_models.User
        fields = ('__all__')


class UserTokenSerializer(serializers.ModelSerializer):

    password =serializers.CharField(write_only=True)
    encoded_jwt = serializers.SerializerMethodField()

    class Meta:
        model = users_models.User
        fields = ('__all__')

    def get_encoded_jwt(self, obj):
        print(obj.pk)
        encoded_jwt = jwt.encode({"pk":obj.pk}, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt



class BooksApartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = books_models.ApartmentDealing
        fields =  ('__all__')
        

class BooksVillaSerializer(serializers.ModelSerializer):

    class Meta:
        model = books_models.RoomDealing
        fields =  ('__all__')


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = contracts_models.ContractBase
        fields =  ('__all__')


class ManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = managements_models.Management
        fields = ('__all__')