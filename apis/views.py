from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from users import models as users_models


class MeView(APIView):
    def get(self, request):
        return Response()
