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
from managements import models as managements_models
from . import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login, logout
import os
import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.urls import reverse


class AllUserView(APIView):
    def get(self, request):
        user = users_models.User.objects.all()
        serializer = serializers.UserSerializer(user, many=True, context={"request":request}).data
        return Response(serializer)

class SocialLoginTokenView(APIView):
    def get(self, request,pk):
        user = users_models.User.objects.get(pk=pk)
        serializer = serializers.UserTokenSerializer(user, context={"request":request}).data
        return Response(serializer)


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


# class SocialLoginView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         # username = "kjhwnsghksk@naver.com"
#         # password = "52848625a"
        
#         if not username:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         # user = authenticate(username=username)
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             encoded_jwt = jwt.encode({"pk":user.pk}, settings.SECRET_KEY, algorithm="HS256")
#             return Response(data={"token":encoded_jwt, "id":user.pk})
#         else:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)

class KakaoException(Exception):
    pass


@api_view(["GET", "PUT"])
def social_login(request):
    try:
        REST_API_KEY = os.environ.get("KAKAO_ID")
        REDIRECT_URI = "https://2a43-112-187-140-235.jp.ngrok.io/api/v1/users/social-login/"
        code = request.GET.get("code")
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}")
        token_json = token_request.json()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}", })
        profile_json = profile_request.json()
        properties = profile_json.get("properties")
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        try:
            user = users_models.User.objects.get(email=email)
            if user.login_method != users_models.User.LOGIN_KAKAO:
                messages.error(request, "다른 경로로 가입되어있는 이메일입니다")
                return redirect("users:login")
        except users_models.User.DoesNotExist:
            user = users_models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=users_models.User.LOGIN_KAKAO,
            )
            user.set_unusable_password()
            user.email_verified = True
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                user.avatar.save(f"{nickname}-avatar",
                                ContentFile(photo_request.content))
        encoded_jwt = jwt.encode({"pk":user.pk}, settings.SECRET_KEY, algorithm="HS256")
        # return render(request, 'app_token.html', {"access_token":access_token, "email":email, "user_pk":get_user.pk})
        login(request, user)
        # return Response(data={"token":encoded_jwt, "id":user.pk})
        return render(request, 'app_token.html', {"user_pk":user.pk})
    except KakaoException:
        return redirect(reverse("users:login"))


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
        print(price)
        area_m2 = int(request.GET.get("area_m2", 0))
        room = request.GET.get("room", 0)
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        if address:
            filter_args["address__contains"] = address
        # filter_args["description__contains"] = description
        if price:
            filter_args["price__lte"] = price
        if area_m2:
            filter_args["area_m2__gte"] = area_m2
        if room:
            filter_args["room"] = room
        if parking:
            filter_args["parking"] = True
        else:
            filter_args["parking"] = False
        if empty:
            filter_args["empty"] = True
        else:
            filter_args["empty"] = False
        if elevator:
            filter_args["elevator"] = True
        else:
            filter_args["elevator"] = False
        if loan:
            filter_args["loan"] = True
        else:
            filter_args["loan"] = False
        if not_finished:
            filter_args["not_finished"] = True
        else:
            filter_args["not_finished"] = False

        print(filter_args)
        lists = books_models.RoomDealing.objects.filter(**filter_args)
        print(lists)
        try:
            lists = books_models.RoomDealing.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksVillaSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
    

class ContractView(APIView):
    def get(self, request):
        contracts = contracts_models.ContractBase.objects.filter(realtor_id=request.user.pk)
        serializer = serializers.ContractSerializer(contracts, many=True, context={"request":request}).data
        return Response(serializer)
    def post(self, request):
        serializer = serializers.ContractSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_contract = serializer.save()
            return Response(serializers.ContractSerializer(new_contract).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractUpdatingView(APIView):
    def get(self, request, pk):
        contract = contracts_models.ContractBase.objects.get(pk=pk)
        serializer = serializers.ContractSerializer(contract, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        contract = contracts_models.ContractBase.objects.get(pk=pk)
        serializer = serializers.ContractSerializer(contract, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractDeletingView(APIView):
    def get(self, request, pk):
        contract = contracts_models.ContractBase.objects.get(pk=pk)
        serializer = serializers.ContractSerializer(contract)
        return Response(serializer.data)

    def delete(self, request, pk):
        contract = contracts_models.ContractBase.objects.get(pk=pk)
        contract.delete()
        return Response()

class ManagementView(APIView):
    def get(self, request):
        managements = managements_models.Management.objects.filter(manager_id = request.user.pk)
        serializer = serializers.ManagementSerializer(managements, many=True, context={"request":request}).data
        return Response(serializer)
    def post(self, request):
        serializer = serializers.ManagementSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_management = serializer.save()
            return Response(serializers.ManagementSerializer(new_management).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagementUpdatingView(APIView):
    def get(self, request, pk):
        management = managements_models.Management.objects.get(pk=pk)
        serializer = serializers.ManagementSerializer(management, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        management = managements_models.Management.objects.get(pk=pk)
        serializer = serializers.ManagementSerializer(management, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagementDeletingView(APIView):
    def get(self, request, pk):
        management = managements_models.Management.objects.get(pk=pk)
        serializer = serializers.ManagementSerializer(management)
        return Response(serializer.data)

    def delete(self, request, pk):
        management = managements_models.Management.objects.get(pk=pk)
        management.delete()
        return Response()