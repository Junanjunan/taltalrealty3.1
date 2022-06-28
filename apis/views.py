import jwt
import uuid
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
from apis.home_url import home_url


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
        return Response(serializers.UserSerializer(request.user, context={"request":request}).data)


class ProfileView(APIView):
    def get(self, request, pk):
        user = users_models.User.objects.get(pk=pk)
        serializer = serializers.UserSerializer(user, context={"request":request}).data
        return Response(serializer)


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

def kakao_login_app(request):
    if settings.DEBUG == True:
        REST_API_KEY = os.environ.get("KAKAO_ID")
        REDIRECT_URI = f"{home_url}/api/v1/login/kakao/callback/"
    else:
        REST_API_KEY = os.environ.get("KAKAO_ID_DEPLOY")
        REDIRECT_URI = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/api/v1/users/social-login/"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code")


def kakao_callback_app(request):
    try:
        if settings.DEBUG == True:
            REST_API_KEY = os.environ.get("KAKAO_ID")
            # REDIRECT_URI = "https://8821-121-130-89-131.jp.ngrok.io/api/v1/users/social-login/"
            REDIRECT_URI = f"{home_url}/api/v1/login/kakao/callback/"
        else:
            REST_API_KEY = os.environ.get("KAKAO_ID_DEPLOY")
            REDIRECT_URI = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/api/v1/users/social-login/"
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
                return redirect("users:login-app")
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
        return render(request, 'app_token.html', {"user_pk":user.pk, 'access_token':encoded_jwt, 'email':email, 'request':request})
    except KakaoException:
        return redirect(reverse("users:login"))


def naver_login_app(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("NAVER_ID")
        # redirect_uri = "https://8358-121-130-89-131.jp.ngrok.io/users/login/naver/callback/"
        # redirect_uri = "https://8821-121-130-89-131.jp.ngrok.io/api/v1/login/naver/callback/"
        redirect_uri = f"{home_url}/api/v1/login/naver/callback/"
    else:
        client_id = os.environ.get("NAVER_ID_DEPLOY")
        redirect_uri = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/users/login/naver/callback/"
    state = uuid.uuid4().hex[:20]
    return redirect(f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}")

def naver_callback_app(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
    else:
        client_id = os.environ.get("NAVER_ID_DEPLOY")
        client_secret = os.environ.get("NAVER_SECRET_DEPLOY")
    code = request.GET.get("code")
    state = request.GET.get("state")
    token_request = requests.post(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"
    )
    token_json = token_request.json()
    access_token = token_json.get("access_token")
    profile_request = requests.get(
        "https://openapi.naver.com/v1/nid/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        }
    )
    profile_json = profile_request.json()
    response = profile_json.get("response")
    print(response)
    email = response.get("email")
    try:
        user = users_models.User.objects.get(email=email)
        if user.login_method != users_models.User.LOGIN_NAVER:
            messages.error(request, "다른 경로로 가입되어있는 이메일입니다")
            return redirect("users:login-app")
    except users_models.User.DoesNotExist:
        user = users_models.User.objects.create(
            email=email,
            username=email,
            login_method=users_models.User.LOGIN_NAVER
        )
        user.set_unusable_password()
        user.email_verified = True
        user.save()
    encoded_jwt = jwt.encode({"pk":user.pk}, settings.SECRET_KEY, algorithm="HS256")
    login(request,user)
    return render(request, 'app_token.html', {"user_pk":user.pk, 'access_token':encoded_jwt, 'email':email, 'request':request})

def github_login_app(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("GH_ID_APP")
        redirect_uri = f"{home_url}/api/v1/login/github/callback/"
    else:
        client_id = os.environ.get("GH_ID_DEPLOY")
        redirect_uri = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/users/login/github/callback/"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


def github_callback_app(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("GH_ID_APP")
        client_secret = os.environ.get("GH_SECRET_APP")
    else:
        client_id = os.environ.get("GH_ID_DEPLOY")
        client_secret = os.environ.get("GH_SECRET_DEPLOY")
    code = request.GET.get("code")
    result = requests.post(
        f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
        headers={"Accept": "application/json"},)
    result_json = result.json()
    access_token = result_json.get("access_token")
    profile_request = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"token {access_token}",
            "Accept": "application/json"})
    profile_json = profile_request.json()
    print(profile_json)
    email = profile_json.get("email")
    bio = profile_json.get("bio")
    bio = "" if bio is None else bio
    try:
        user = users_models.User.objects.get(email=email)
        if user.login_method != users_models.User.LOGIN_GITHUB:
            messages.error(request, "다른 경로로 가입되어있는 이메일입니다")
            return redirect("users:login-app")
    except users_models.User.DoesNotExist:
        user = users_models.User.objects.create(
            username=email, email=email,
            bio=bio, login_method= users_models.User.LOGIN_GITHUB)
        user.set_unusable_password()
        user.email_verified = True
        user.save()
    encoded_jwt = jwt.encode({"pk":user.pk}, settings.SECRET_KEY, algorithm="HS256")
    login(request,user)
    return render(request, 'app_token.html', {"user_pk":user.pk, 'access_token':encoded_jwt, 'email':email, 'request':request})


def social_logout(request):
    logout(request)
    return redirect(reverse("core:home"))

"""Apartment Start"""

class BooksApartmentDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.ApartmentDealing.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksApartmentDealingSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksApartmentDealingSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksApartmentDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksApartmentDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.ApartmentDealing.objects.get(pk=pk)
        serializer = serializers.BooksApartmentDealingSerializer(book, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.ApartmentDealing.objects.get(pk=pk)
        serializer = serializers.BooksApartmentDealingSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksApartmentDealingDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.ApartmentDealing.objects.get(pk=pk)
        serializer = serializers.BooksApartmentDealingSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.ApartmentDealing.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksApartmentDealingSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        price = int(request.GET.get("price", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        room = request.GET.get("room", 0)
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        # filter_args["realtor"] = request.user
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
        lists = books_models.ApartmentDealing.objects.filter(**filter_args)
        print(lists)
        try:
            lists = books_models.ApartmentDealing.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksApartmentDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Apartment Finish"""

# class BooksApartmentDealingView(APIView):
#     def get(self, request):
#         books = books_models.ApartmentDealing.objects.all()
#         serializer = serializers.BooksApartmentSerializer(books, many=True, context={"request":request}).data
#         return Response(serializer)

class BooksApartmentDealingDetailView(APIView):
    def get(self, request, pk):
        books = books_models.ApartmentDealing.objects.get(pk=pk)
        serializer = serializers.BooksApartmentSerializer(books, context={"request":request}).data
        return Response(serializer)

class BooksVillaDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.RoomDealing.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksVillaDealingSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksVillaDealingSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksVillaDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksVillaDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        serializer = serializers.BooksVillaDealingSerializer(book, context={"request":request}).data
        # updated_villa = serializer.save()
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        serializer = serializers.BooksVillaDealingSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksVillaDealingDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        serializer = serializers.BooksVillaDealingSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksVillaDealingSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        price = int(request.GET.get("price", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        room = request.GET.get("room", 0)
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        # filter_args["realtor"] = request.user
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
        serializer = serializers.BooksVillaDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)


"""Officetel Start"""

class BooksOfficetelDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.OfficetelDealing.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksOfficetelDealingSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksOfficetelDealingSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksOfficetelDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksOfficetelDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.OfficetelDealing.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelDealingSerializer(book, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.OfficetelDealing.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelDealingSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksOfficetelDealingDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.OfficetelDealing.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelDealingSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.OfficetelDealing.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksOfficetelDealingSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        price = int(request.GET.get("price", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        room = request.GET.get("room", 0)
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if address:
            filter_args["address__contains"] = address
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
        lists = books_models.OfficetelDealing.objects.filter(**filter_args)
        try:
            lists = books_models.OfficetelDealing.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksOfficetelDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Officetel Finish"""


"""Store Start"""

class BooksStoreDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.StoreDealing.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksStoreDealingSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksStoreDealingSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksStoreDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksStoreDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.StoreDealing.objects.get(pk=pk)
        serializer = serializers.BooksStoreDealingSerializer(book, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.StoreDealing.objects.get(pk=pk)
        serializer = serializers.BooksStoreDealingSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksStoreDealingDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.StoreDealing.objects.get(pk=pk)
        serializer = serializers.BooksStoreDealingSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.StoreDealing.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksStoreDealingSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        price = int(request.GET.get("price", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if address:
            filter_args["address__contains"] = address
        if price:
            filter_args["price__lte"] = price
        if area_m2:
            filter_args["area_m2__gte"] = area_m2
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
        lists = books_models.StoreDealing.objects.filter(**filter_args)

        try:
            lists = books_models.StoreDealing.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksStoreDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Store Finish"""

"""Building Start"""

class BooksBuildingDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.BuildingDealing.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksBuildingDealingSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksBuildingDealingSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksBuildingDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksBuildingDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.BuildingDealing.objects.get(pk=pk)
        serializer = serializers.BooksBuildingDealingSerializer(book, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.BuildingDealing.objects.get(pk=pk)
        serializer = serializers.BooksBuildingDealingSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksBuildingDealingDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.BuildingDealing.objects.get(pk=pk)
        serializer = serializers.BooksBuildingDealingSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.BuildingDealing.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksBuildingDealingSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        price = int(request.GET.get("price", 0))
        land_m2 = float(request.GET.get("land_m2", 0))
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if address:
            filter_args["address__contains"] = address
        if price:
            filter_args["price__lte"] = price
        if land_m2:
            filter_args["land_m2__gte"] = land_m2
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

        lists = books_models.BuildingDealing.objects.filter(**filter_args)

        try:
            lists = books_models.BuildingDealing.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksBuildingDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Building Finish"""


"""Apartment Lease Start"""

class BooksApartmentLeaseView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.ApartmentLease.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksApartmentLeaseSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksApartmentLeaseSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksApartmentLeaseSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksApartmentLeaseUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.ApartmentLease.objects.get(pk=pk)
        serializer = serializers.BooksApartmentLeaseSerializer(book, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.ApartmentLease.objects.get(pk=pk)
        serializer = serializers.BooksApartmentLeaseSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksApartmentLeaseDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.ApartmentLease.objects.get(pk=pk)
        serializer = serializers.BooksApartmentLeaseSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.ApartmentLease.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksApartmentLeaseSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        area_m2 = int(request.GET.get("area_m2", 0))
        deposit = int(request.GET.get("deposit", 0))
        month_fee = int(request.GET.get("month_fee", 0))
        room = request.GET.get("room", 0)
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if address:
            filter_args["address__contains"] = address
        if deposit:
            filter_args["deposit__lte"] = deposit
        if month_fee:
            filter_args["month_fee__lte"] = month_fee
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

        try:
            lists = books_models.ApartmentLease.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksApartmentLeaseSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Apartment Lease Finish"""

"""Villa Lease Start"""
class BooksVillaLeaseView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.RoomLease.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksVillaLeaseSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksVillaLeaseSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksVillaLeaseSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksVillaLeaseUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.RoomLease.objects.get(pk=pk)
        serializer = serializers.BooksVillaLeaseSerializer(book, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.RoomLease.objects.get(pk=pk)
        serializer = serializers.BooksVillaLeaseSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksVillaLeaseDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.RoomLease.objects.get(pk=pk)
        serializer = serializers.BooksVillaLeaseSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.RoomLease.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksVillaLeaseSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        deposit = int(request.GET.get("deposit", 0))
        month_fee = int(request.GET.get("month_fee", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        room = request.GET.get("room", 0)
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if address:
            filter_args["address__contains"] = address
        if deposit:
            filter_args["deposit__lte"] = deposit
        if month_fee:
            filter_args["month_fee__lte"] = month_fee
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

        try:
            lists = books_models.RoomLease.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksVillaLeaseSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Villa Lease Finish"""


"""Officetel Lease Start"""

class BooksOfficetelLeaseView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.OfficetelLease.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksOfficetelLeaseSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksOfficetelLeaseSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksOfficetelLeaseSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksOfficetelLeaseUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.OfficetelLease.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelLeaseSerializer(book, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.OfficetelLease.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelLeaseSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksOfficetelLeaseDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.OfficetelLease.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelLeaseSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.OfficetelLease.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksOfficetelLeaseSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        deposit = int(request.GET.get("deposit", 0))
        month_fee = int(request.GET.get("month_fee", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        room = request.GET.get("room", 0)
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if address:
            filter_args["address__contains"] = address
        if deposit:
            filter_args["deposit__lte"] = deposit
        if month_fee:
            filter_args["month_fee__lte"] = month_fee
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
        
        try:
            lists = books_models.OfficetelLease.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksOfficetelLeaseSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Officetel Lease Finish"""


"""Store Lease Start"""

class BooksStoreLeaseView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.StoreLease.objects.filter(realtor_id=user.pk)
        serializer = serializers.BooksStoreLeaseSerializer(books, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksStoreLeaseSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksStoreLeaseSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksStoreLeaseUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.StoreLease.objects.get(pk=pk)
        serializer = serializers.BooksStoreLeaseSerializer(book, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.StoreLease.objects.get(pk=pk)
        serializer = serializers.BooksStoreLeaseSerializer(book, data=request.data, partial=True, context={"request":request})
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BooksStoreLeaseDeletingView(APIView):
    def get(self, request, pk):
        book = books_models.StoreLease.objects.get(pk=pk)
        serializer = serializers.BooksStoreLeaseSerializer(book)
        return Response(serializer.data)

    def delete(self, request, pk):
        book = books_models.StoreLease.objects.get(pk=pk)
        book.delete()
        return Response()


class BooksStoreLeaseSearchingView(APIView):
    def get(self, request):
        realtor_id = request.GET.get("realtor_id")
        address = request.GET.get("address")
        deposit = int(request.GET.get("deposit", 0))
        month_fee = int(request.GET.get("month_fee", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        empty = request.GET.get("empty")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if address:
            filter_args["address__contains"] = address
        if deposit:
            filter_args["deposit__lte"] = deposit
        if month_fee:
            filter_args["month_fee__lte"] = month_fee
        if area_m2:
            filter_args["area_m2__gte"] = area_m2
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

        try:
            lists = books_models.StoreLease.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.BooksStoreLeaseSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Store Lease Finish"""

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