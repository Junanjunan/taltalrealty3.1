import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users import models as users_models
from books import models as books_models
from contracts import models as contracts_models
from . import serializers


class MeView(APIView):
    def get(self, request):
        return Response(serializers.UserSerializer(request.user).data)


class TestView(APIView):
    def get(self, request):
        user = users_models.User.objects.get(pk=1)
        serializer = serializers.UserSerializer(user).data
        return Response(serializer)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode({"pk":user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response(data={"token":encoded_jwt, "id":user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class BooksApartmentDealingView(APIView):
    def get(self, request):
        books = books_models.ApartmentDealing.objects.all()
        serializer = serializers.BooksApartmentSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

class BooksApartmentDealingDetailView(APIView):
    def get(self, request, pk):
        books = books_models.ApartmentDealing.objects.get(pk=pk)
        serializer = serializers.BooksApartmentSerializer(books, context={"request":request}).data
        return Response(serializer)

class BooksVillaDealingView(APIView):
    def get(self, request):
        books = books_models.RoomDealing.objects.all()
        serializer = serializers.BooksVillaSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksVillaSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksVillaSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksVillaDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        serializer = serializers.BooksVillaSerializer(book, context={"request":request}).data
        # updated_villa = serializer.save()
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        serializer = serializers.BooksVillaSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksVillaDealingDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        serializer = serializers.BooksVillaSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksVillaDealingSearchingView(APIView):
    def get(self, request):
        address = request.GET.get("address")
        price = int(request.GET.get("price", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        room = request.GET.get("room", 0)
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
        description = request.GET.get("description")
    
        filter_args = {}
        filter_args["address__contains"] = address
        filter_args["description__contains"] = description
        filter_args["price__lte"] = price
        filter_args["area_m2__gte"] = area_m2
        filter_args["room__contains"] = room
        if parking == "on":
            filter_args["parking"] = True
        if elevator == "on":
            filter_args["elevator"] = True
        if empty == "on":
            filter_args["empty"] = True
        if not_finished == "on":
            filter_args["not_finished"] = True
        try:
            lists = books_models.RoomDealing.objects.filter(**filter_args)
        except:
            lists = books_models.RoomDealing.objects.all()
        serializer = serializers.BooksVillaSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
    

class ContractView(APIView):
    def get(self, request):
        contracts = contracts_models.ContractBase.objects.all()
        serializer = serializers.ContractSerializer(contracts, many=True, context={"request":request}).data
        return Response(serializer)