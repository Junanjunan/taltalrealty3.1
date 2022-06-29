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


"""Dealing"""

class BooksApartmentDealingSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.ApartmentDealing
        fields = ('__all__')


class BooksVillaDealingSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.RoomDealing
        fields =  ('__all__')


class BooksOfficetelDealingSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.OfficetelDealing
        fields =  ('__all__')


class BooksStoreDealingSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.StoreDealing
        fields =  ('__all__')


class BooksBuildingDealingSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.BuildingDealing
        fields =  ('__all__')


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = contracts_models.ContractBase
        fields =  ('__all__')

"""Lease"""

class BooksApartmentLeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.ApartmentLease
        fields = ('__all__')

class BooksVillaLeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.RoomLease
        fields = ('__all__')

class BooksOfficetelLeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.OfficetelLease
        fields = ('__all__')

class BooksStoreLeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = books_models.StoreLease
        fields = ('__all__')


class ManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = managements_models.Management
        fields = ('__all__')