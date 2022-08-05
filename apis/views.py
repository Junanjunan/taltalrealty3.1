import jwt
import uuid
import os
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.urls import reverse
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from users import models as users_models
from books import models as books_models
from customers import models as customers_models
from contracts import models as contracts_models
from managements import models as managements_models
from apis.home_url import home_url
from components.search_filter_for_app import search_filter_for_app
from . import serializers


class AllUserView(APIView):
    def get(self, request):
        user = users_models.User.objects.all()
        serializer = serializers.UserSerializer(
            user, 
            many=True, 
            context={"request":request}
        ).data
        return Response(serializer)


class SocialLoginTokenView(APIView):
    def get(self, request,pk):
        user = users_models.User.objects.get(pk=pk)
        serializer = serializers.UserTokenSerializer(
            user, 
            context={"request":request}
        ).data
        return Response(serializer)


class MeView(APIView):
    def get(self, request):
        return Response(serializers.UserSerializer(
            request.user,
            context={"request":request}
            ).data)


class ProfileView(APIView):
    def get(self, request, pk):
        user = users_models.User.objects.get(pk=pk)
        serializer = serializers.UserSerializer(
            user, 
            context={"request":request}
        ).data
        return Response(serializer)

    def post(self, request, pk):
        password = request.data["password"]
        user = users_models.User.objects.get(pk=pk)
        if check_password(password, user.password):     # https://ssungkang.tistory.com/entry/DjangoUser-%EB%B9%84%EB%B0%80%EB%B2%88%ED%98%B8-%EB%B3%80%EA%B2%BD%ED%95%98%EA%B8%B0-checkpassword
            new_password = request.data["new_password"]
            user.set_password(new_password)
            user.save()
        else:
            print("오류오류")
        return Response()

    def delete(self, request, pk):
        user = users_models.User.objects.get(pk=pk)
        user.delete()
        return Response()

class UpdateStatusView(APIView):
    def get(self, request, pk):
        user = users_models.User.objects.get(pk=pk)
        serializer = serializers.UserSerializer(
            user,
            context={"request":request}
        ).data
        return Response(serializer)

    def post(self, request, pk):
        office = request.data["office"]
        tel = request.data["tel"]
        user= users_models.User.objects.get(pk=pk)
        user.office = office
        user.tel = tel
        user.save()
        serializer = serializers.UserSerializer(
            user,
            context={"request":request}
        ) .data
        return Response(serializer)


class TestView(APIView):
    def get(self, request):
        user = users_models.User.objects.get(pk=1)
        serializer = serializers.UserSerializer(user).data
        return Response(serializer)


class SignUpView(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(request.data["password"])
            new_user.save()
            user_id = new_user.user_id
            user = users_models.User.objects.get(pk=user_id)
            user.verify_email()
            return Response(serializers.UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk":user.pk}, 
                settings.SECRET_KEY, 
                algorithm="HS256"
            )
            return Response(data={"token":encoded_jwt, "id":user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class KakaoException(Exception):
    pass

def kakao_login_app(request):
    if settings.DEBUG == True:
        REST_API_KEY = os.environ.get("KAKAO_ID")
        REDIRECT_URI = f"{home_url}/api/v1/login/kakao/callback/"
    else:
        REST_API_KEY = os.environ.get("KAKAO_ID_DEPLOY_APP")
        REDIRECT_URI = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/api/v1/login/kakao/callback/"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code")


def kakao_callback_app(request):
    try:
        if settings.DEBUG == True:
            REST_API_KEY = os.environ.get("KAKAO_ID")
            REDIRECT_URI = f"{home_url}/api/v1/login/kakao/callback/"
        else:
            REST_API_KEY = os.environ.get("KAKAO_ID_DEPLOY_APP")
            REDIRECT_URI = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/api/v1/login/kakao/callback/"
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
        login(request, user)
        return render(request, 'app_token.html', {"user_pk":user.pk, 'access_token':encoded_jwt, 'email':email, 'request':request})
    except KakaoException:
        return redirect(reverse("users:login"))


def naver_login_app(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("NAVER_ID")
        redirect_uri = f"{home_url}/api/v1/login/naver/callback/"
    else:
        client_id = os.environ.get("NAVER_ID_DEPLOY_APP")
        redirect_uri = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/api/v1/login/naver/callback/"
    state = uuid.uuid4().hex[:20]
    return redirect(f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&state={state}")

def naver_callback_app(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("NAVER_ID")
        client_secret = os.environ.get("NAVER_SECRET")
    else:
        client_id = os.environ.get("NAVER_ID_DEPLOY_APP")
        client_secret = os.environ.get("NAVER_SECRET_DEPLOY_APP")
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
    encoded_jwt = jwt.encode(
        {"pk":user.pk}, 
        settings.SECRET_KEY, 
        algorithm="HS256"
    )
    login(request,user)
    return render(request, 'app_token.html', {
        "user_pk":user.pk, 
        'access_token':encoded_jwt, 
        'email':email, 
        'request':request
        })

def github_login_app(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("GH_ID_APP")
        redirect_uri = f"{home_url}/api/v1/login/github/callback/"
    else:
        client_id = os.environ.get("GH_ID_DEPLOY_APP")
        redirect_uri = "http://taltalrealty31-dev.ap-northeast-2.elasticbeanstalk.com/api/v1/login/github/callback/"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")


def github_callback_app(request):
    if settings.DEBUG == True:
        client_id = os.environ.get("GH_ID_APP")
        client_secret = os.environ.get("GH_SECRET_APP")
    else:
        client_id = os.environ.get("GH_ID_DEPLOY_APP")
        client_secret = os.environ.get("GH_SECRET_DEPLOY_APP")
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
    encoded_jwt = jwt.encode(
        {"pk":user.pk}, 
        settings.SECRET_KEY, 
        algorithm="HS256"
        )
    login(request,user)
    return render(request, 'app_token.html', {
        "user_pk":user.pk, 
        'access_token':encoded_jwt, 
        'email':email, 
        'request':request}
        )


def social_logout(request):
    logout(request)
    return redirect(reverse("core:home"))

"""Apartment Start"""

class BooksApartmentDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.ApartmentDealing.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksApartmentDealingSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksApartmentDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksApartmentDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksApartmentDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.ApartmentDealing.objects.get(pk=pk)
        serializer = serializers.BooksApartmentDealingSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.ApartmentDealing.objects.get(pk=pk)
        serializer = serializers.BooksApartmentDealingSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.ApartmentDealing.objects.filter(**filter_args)
        serializer = serializers.BooksApartmentDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)

class BooksApartmentDealingDetailView(APIView):
    def get(self, request, pk):
        books = books_models.ApartmentDealing.objects.get(pk=pk)
        serializer = serializers.BooksApartmentSerializer(books, context={"request":request}).data
        return Response(serializer)
"""Apartment Finish"""



class BooksVillaDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.RoomDealing.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksVillaDealingSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksVillaDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksVillaDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksVillaDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        serializer = serializers.BooksVillaDealingSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.RoomDealing.objects.get(pk=pk)
        serializer = serializers.BooksVillaDealingSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.RoomDealing.objects.filter(**filter_args)
        serializer = serializers.BooksVillaDealingSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)


"""Officetel Start"""

class BooksOfficetelDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.OfficetelDealing.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksOfficetelDealingSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksOfficetelDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksOfficetelDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksOfficetelDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.OfficetelDealing.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelDealingSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.OfficetelDealing.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelDealingSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.OfficetelDealing.objects.filter(**filter_args)
        serializer = serializers.BooksOfficetelDealingSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)
"""Officetel Finish"""

"""Store Start"""

class BooksStoreDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.StoreDealing.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksStoreDealingSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksStoreDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksStoreDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksStoreDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.StoreDealing.objects.get(pk=pk)
        serializer = serializers.BooksStoreDealingSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.StoreDealing.objects.get(pk=pk)
        serializer = serializers.BooksStoreDealingSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.StoreDealing.objects.filter(**filter_args)
        serializer = serializers.BooksStoreDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Store Finish"""

"""Building Start"""

class BooksBuildingDealingView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.BuildingDealing.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksBuildingDealingSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksBuildingDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksBuildingDealingSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksBuildingDealingUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.BuildingDealing.objects.get(pk=pk)
        serializer = serializers.BooksBuildingDealingSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.BuildingDealing.objects.get(pk=pk)
        serializer = serializers.BooksBuildingDealingSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.BuildingDealing.objects.filter(**filter_args)
        serializer = serializers.BooksBuildingDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)
"""Building Finish"""


"""Apartment Lease Start"""

class BooksApartmentLeaseView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.ApartmentLease.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksApartmentLeaseSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksApartmentLeaseSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksApartmentLeaseSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksApartmentLeaseUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.ApartmentLease.objects.get(pk=pk)
        serializer = serializers.BooksApartmentLeaseSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.ApartmentLease.objects.get(pk=pk)
        serializer = serializers.BooksApartmentLeaseSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.ApartmentLease.objects.filter(**filter_args)
        serializer = serializers.BooksApartmentLeaseSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)
"""Apartment Lease Finish"""

"""Villa Lease Start"""
class BooksVillaLeaseView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.RoomLease.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksVillaLeaseSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksVillaLeaseSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksVillaLeaseSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksVillaLeaseUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.RoomLease.objects.get(pk=pk)
        serializer = serializers.BooksVillaLeaseSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.RoomLease.objects.get(pk=pk)
        serializer = serializers.BooksVillaLeaseSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.RoomLease.objects.filter(**filter_args)
        serializer = serializers.BooksVillaLeaseSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)
"""Villa Lease Finish"""


"""Officetel Lease Start"""

class BooksOfficetelLeaseView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.OfficetelLease.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksOfficetelLeaseSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksOfficetelLeaseSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksOfficetelLeaseSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksOfficetelLeaseUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.OfficetelLease.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelLeaseSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.OfficetelLease.objects.get(pk=pk)
        serializer = serializers.BooksOfficetelLeaseSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.OfficetelLease.objects.filter(**filter_args)
        serializer = serializers.BooksOfficetelLeaseSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)
"""Officetel Lease Finish"""


"""Store Lease Start"""

class BooksStoreLeaseView(APIView):
    def get(self, request):
        user = request.user
        books = books_models.StoreLease.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.BooksStoreLeaseSerializer(
            books, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.BooksStoreLeaseSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_villa = serializer.save()
            return Response(serializers.BooksStoreLeaseSerializer(new_villa).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BooksStoreLeaseUpdatingView(APIView):
    def get(self, request, pk):
        book = books_models.StoreLease.objects.get(pk=pk)
        serializer = serializers.BooksStoreLeaseSerializer(
            book, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        book = books_models.StoreLease.objects.get(pk=pk)
        serializer = serializers.BooksStoreLeaseSerializer(
            book, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        filter_args = search_filter_for_app(request)
        lists = books_models.StoreLease.objects.filter(**filter_args)
        serializer = serializers.BooksStoreLeaseSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)
"""Store Lease Finish"""

"""Customer Apartment Dealing Start"""

class CustomerApartmentDealingView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.ApartmentDealingCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerApartmentDealingSerializer(
            customers, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerApartmentDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerApartmentDealingSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerApartmentDealingUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ApartmentDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentDealingSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.ApartmentDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentDealingSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerApartmentDealingDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ApartmentDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentDealingSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.ApartmentDealingCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerApartmentDealingSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.ApartmentDealingCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerApartmentDealingSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Apartment Dealing Finish"""

"""Customer Building Dealing Start"""

class CustomerBuildingDealingView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.BuildingDealingCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerBuildingDealingSerializer(
            customers, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerBuildingDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerBuildingDealingSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerBuildingDealingUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.BuildingDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerBuildingDealingSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.BuildingDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerBuildingDealingSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerBuildingDealingDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.BuildingDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerBuildingDealingSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.BuildingDealingCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerBuildingDealingSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.BuildingDealingCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerBuildingDealingSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Building Dealing Finish"""

"""Customer Villa Dealing Start"""

class CustomerVillaDealingView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.HouseDealingCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerVillaDealingSerializer(
            customers,
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerVillaDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerVillaDealingSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerVillaDealingUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.HouseDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerVillaDealingSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.HouseDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerVillaDealingSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerVillaDealingDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.HouseDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerVillaDealingSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.HouseDealingCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerVillaDealingSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.HouseDealingCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerVillaDealingSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Villa Dealing Finish"""

"""Customer Officetel Dealing Start"""

class CustomerOfficetelDealingView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.OfficetelDealingCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerOfficetelDealingSerializer(
            customers, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerOfficetelDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerOfficetelDealingSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerOfficetelDealingUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.OfficetelDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerOfficetelDealingSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.OfficetelDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerOfficetelDealingSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerOfficetelDealingDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.OfficetelDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerOfficetelDealingSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.OfficetelDealingCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerOfficetelDealingSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.OfficetelDealingCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerOfficetelDealingSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Officetel Dealing Finish"""

"""Customer Store Dealing Start"""

class CustomerStoreDealingView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.ShopDealingCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerStoreDealingSerializer(
            customers, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerStoreDealingSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerStoreDealingSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerStoreDealingUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ShopDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerStoreDealingSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.ShopDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerStoreDealingSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerStoreDealingDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ShopDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerStoreDealingSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.ShopDealingCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerStoreDealingSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.ShopDealingCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerStoreDealingSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Store Dealing Finish"""

"""Customer Apartment Lease Start"""

class CustomerApartmentLeaseView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.ApartmentLeaseCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerApartmentLeaseSerializer(
            customers, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerApartmentLeaseSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerApartmentLeaseSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerApartmentLeaseUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ApartmentLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentLeaseSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.ApartmentLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentLeaseSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerApartmentLeaseDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ApartmentLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentLeaseSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.ApartmentLeaseCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerApartmentLeaseSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.ApartmentLeaseCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerApartmentLeaseSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Apartment Lease Finish"""

"""Customer Villa Lease Start"""

class CustomerVillaLeaseView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.HouseLeaseCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerVillaLeaseSerializer(
            customers, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerVillaLeaseSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerVillaLeaseSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerVillaLeaseUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.HouseLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerVillaLeaseSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.HouseLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerVillaLeaseSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerVillaLeaseDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.HouseLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerVillaLeaseSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.HouseLeaseCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerVillaLeaseSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.HouseLeaseCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerVillaLeaseSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Villa Lease Finish"""

"""Customer Officetel Lease Start"""

class CustomerOfficetelLeaseView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.OfficetelLeaseCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerOfficetelLeaseSerializer(
            customers, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerOfficetelLeaseSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerOfficetelLeaseSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerOfficetelLeaseUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.OfficetelLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerOfficetelLeaseSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.OfficetelLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerOfficetelLeaseSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerOfficetelLeaseDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.OfficetelLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerOfficetelLeaseSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.OfficetelLeaseCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerOfficetelLeaseSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.OfficetelLeaseCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerOfficetelLeaseSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Officetel Lease Finish"""

"""Customer Store Lease Start"""

class CustomerStoreLeaseView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.ShopLeaseCustomer.objects.filter(realtor_id=user.pk, not_finished=True)
        serializer = serializers.CustomerStoreLeaseSerializer(
            customers, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerStoreLeaseSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerStoreLeaseSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerStoreLeaseUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ShopLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerStoreLeaseSerializer(
            customer, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.ShopLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerStoreLeaseSerializer(
            customer, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerStoreLeaseDeletingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ShopLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerStoreLeaseSerializer(customer)
        return Response(serializer.data)

    def delete(self, request, pk):
        customer = customers_models.ShopLeaseCustomer.objects.get(pk=pk)
        customer.delete()
        return Response()


class CustomerStoreLeaseSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = customers_models.ShopLeaseCustomer.objects.filter(**filter_args)
        serializer = serializers.CustomerStoreLeaseSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

"""Customer Store Lease Finish"""


class ContractView(APIView):
    def get(self, request):
        contracts = contracts_models.ContractBase.objects.filter(realtor_id=request.user.pk, not_finished=True)
        serializer = serializers.ContractSerializer(
            contracts, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)
    def post(self, request):
        serializer = serializers.ContractSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_contract = serializer.save()
            return Response(serializers.ContractSerializer(new_contract).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContractSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = contracts_models.ContractBase.objects.filter(**filter_args)
        serializer = serializers.ContractSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

class ContractUpdatingView(APIView):
    def get(self, request, pk):
        contract = contracts_models.ContractBase.objects.get(pk=pk)
        serializer = serializers.ContractSerializer(
            contract, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        contract = contracts_models.ContractBase.objects.get(pk=pk)
        serializer = serializers.ContractSerializer(
            contract, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
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
        managements = managements_models.Management.objects.filter(realtor_id = request.user.pk)
        serializer = serializers.ManagementSerializer(
            managements, 
            many=True, 
            context={"request":request}
            ).data
        return Response(serializer)
    def post(self, request):
        serializer = serializers.ManagementSerializer(
            data=request.data, 
            context={"request":request}
            )
        if serializer.is_valid():
            new_management = serializer.save()
            return Response(serializers.ManagementSerializer(new_management).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagementUpdatingView(APIView):
    def get(self, request, pk):
        management = managements_models.Management.objects.get(pk=pk)
        serializer = serializers.ManagementSerializer(
            management, 
            context={"request":request}
            ).data
        return Response(serializer)
    def put(self, request, pk):
        management = managements_models.Management.objects.get(pk=pk)
        serializer = serializers.ManagementSerializer(
            management, 
            data=request.data, 
            partial=True, 
            context={"request":request}
            )
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagementSearchingView(APIView):
    def get(self, request):
        filter_args = search_filter_for_app(request)
        lists = managements_models.Management.objects.filter(**filter_args)
        serializer = serializers.ManagementSerializer(
            lists, 
            many=True, 
            context={"request":request}
            )
        return Response(serializer.data)

class ManagementDeletingView(APIView):
    def get(self, request, pk):
        management = managements_models.Management.objects.get(pk=pk)
        serializer = serializers.ManagementSerializer(management)
        return Response(serializer.data)

    def delete(self, request, pk):
        management = managements_models.Management.objects.get(pk=pk)
        management.delete()
        return Response()