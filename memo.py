import jwt
import uuid
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users import models as users_models
from customers import models as customers_models
from contracts import models as contracts_models
from managements import models as managements_models
from apis import serializers
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


"""Customer Apartment Dealing Start"""

class CustomerApartmentDealingView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.ApartmentDealingCustomer.objects.filter(realtor_id=user.pk)
        serializer = serializers.CustomerApartmentDealingSerializer(customers, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerApartmentDealingSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerApartmentDealingSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerApartmentDealingUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ApartmentDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentDealingSerializer(customer, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.ApartmentDealingCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentDealingSerializer(customer, data=request.data, partial=True, context={"request":request})
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
        realtor_id = request.GET.get("realtor_id")
        price = int(request.GET.get("price", 0))
        room = request.GET.get("room", 0)
        area_m2 = int(request.GET.get("area_m2", 0))
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
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
        if elevator:
            filter_args["elevator"] = True
        else:
            filter_args["elevator"] = False
        if not_finished:
            filter_args["not_finished"] = True
        else:
            filter_args["not_finished"] = False

        try:
            lists = customers_models.ApartmentDealingCustomer.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.CustomerApartmentDealingSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)

"""Customer Apartment Dealing Finish"""