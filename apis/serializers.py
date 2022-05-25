from rest_framework import serializers
from users import models as users_models
from books import models as books_models
from contracts import models as contracts_models


class UserSerializer(serializers.ModelSerializer):

    password =serializers.CharField(write_only=True)

    class Meta:
        model = users_models.User
        fields = ('__all__')


class BooksApartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = books_models.ApartmentDealing
        fields =  ('__all__')



class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = contracts_models.ContractBase
        fields =  ('__all__')
