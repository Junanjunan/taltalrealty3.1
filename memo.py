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

"""Customer Apartment Lease Start"""

class CustomerApartmentLeaseView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.ApartmentLeaseCustomer.objects.filter(realtor_id=user.pk)
        serializer = serializers.CustomerApartmentLeaseSerializer(customers, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerApartmentLeaseSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerApartmentLeaseSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerApartmentLeaseUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ApartmentLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentLeaseSerializer(customer, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.ApartmentLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerApartmentLeaseSerializer(customer, data=request.data, partial=True, context={"request":request})
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
        realtor_id = request.GET.get("realtor_id")
        guest_phone = request.GET.get("guest_phone")
        room = request.GET.get("room", 0)
        deposit = int(request.GET.get("deposit", 0))
        month_fee = int(request.GET.get("month_fee", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if guest_phone:
            filter_args["guest_phone__contains"] = guest_phone
        if area_m2:
            filter_args["area_m2__gte"] = area_m2
        if room:
            filter_args["room"] = room
        if deposit:
            filter_args["deposit__lte"] = deposit
        if month_fee:
            filter_args["month_fee__lte"] = month_fee
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
            lists = customers_models.ApartmentLeaseCustomer.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.CustomerApartmentLeaseSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)

"""Customer Apartment Lease Finish"""

"""Customer Villa Lease Start"""

class CustomerVillaLeaseView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.HouseLeaseCustomer.objects.filter(realtor_id=user.pk)
        serializer = serializers.CustomerVillaLeaseSerializer(customers, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerVillaLeaseSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerVillaLeaseSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerVillaLeaseUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.HouseLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerVillaLeaseSerializer(customer, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.HouseLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerVillaLeaseSerializer(customer, data=request.data, partial=True, context={"request":request})
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
        realtor_id = request.GET.get("realtor_id")
        guest_phone = request.GET.get("guest_phone")
        room = request.GET.get("room", 0)
        deposit = int(request.GET.get("deposit", 0))
        month_fee = int(request.GET.get("month_fee", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if guest_phone:
            filter_args["guest_phone__contains"] = guest_phone
        if area_m2:
            filter_args["area_m2__gte"] = area_m2
        if room:
            filter_args["room"] = room
        if deposit:
            filter_args["deposit__lte"] = deposit
        if month_fee:
            filter_args["month_fee__lte"] = month_fee
        if parking:
            filter_args["parking"] = True
        else:
            filter_args["parking"] = False
        if elevator:
            filter_args["elevator"] = True
        else:
            filter_args["elevator"] = False
        if elevator:
            filter_args["loan"] = True
        else:
            filter_args["loan"] = False
        if not_finished:
            filter_args["not_finished"] = True
        else:
            filter_args["not_finished"] = False

        try:
            lists = customers_models.HouseLeaseCustomer.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.CustomerVillaLeaseSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)

"""Customer Villa Lease Finish"""

"""Customer Officetel Lease Start"""

class CustomerOfficetelLeaseView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.OfficetelLeaseCustomer.objects.filter(realtor_id=user.pk)
        serializer = serializers.CustomerOfficetelLeaseSerializer(customers, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerOfficetelLeaseSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerOfficetelLeaseSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerOfficetelLeaseUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.OfficetelLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerOfficetelLeaseSerializer(customer, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.OfficetelLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerOfficetelLeaseSerializer(customer, data=request.data, partial=True, context={"request":request})
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
        realtor_id = request.GET.get("realtor_id")
        guest_phone = request.GET.get("guest_phone")
        room = request.GET.get("room", 0)
        deposit = int(request.GET.get("deposit", 0))
        month_fee = int(request.GET.get("month_fee", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        loan = request.GET.get("loan")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if guest_phone:
            filter_args["guest_phone__contains"] = guest_phone
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
        if elevator:
            filter_args["elevator"] = True
        else:
            filter_args["elevator"] = False
        if elevator:
            filter_args["loan"] = True
        else:
            filter_args["loan"] = False
        if not_finished:
            filter_args["not_finished"] = True
        else:
            filter_args["not_finished"] = False

        try:
            lists = customers_models.OfficetelLeaseCustomer.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.CustomerOfficetelLeaseSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)

"""Customer Officetel Lease Finish"""

"""Customer Store Lease Start"""

class CustomerStoreLeaseView(APIView):
    def get(self, request):
        user = request.user
        customers = customers_models.ShopLeaseCustomer.objects.filter(realtor_id=user.pk)
        serializer = serializers.CustomerStoreLeaseSerializer(customers, many=True, context={"request":request}).data
        return Response(serializer)

    def post(self, request):
        serializer = serializers.CustomerStoreLeaseSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            new_customer = serializer.save()
            return Response(serializers.CustomerStoreLeaseSerializer(new_customer).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerStoreLeaseUpdatingView(APIView):
    def get(self, request, pk):
        customer = customers_models.ShopLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerStoreLeaseSerializer(customer, context={"request":request}).data
        return Response(serializer)
    def put(self, request, pk):
        customer = customers_models.ShopLeaseCustomer.objects.get(pk=pk)
        serializer = serializers.CustomerStoreLeaseSerializer(customer, data=request.data, partial=True, context={"request":request})
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
        realtor_id = request.GET.get("realtor_id")
        guest_phone = request.GET.get("guest_phone")
        deposit = int(request.GET.get("deposit", 0))
        month_fee = int(request.GET.get("month_fee", 0))
        area_m2 = int(request.GET.get("area_m2", 0))
        parking = request.GET.get("parking")
        elevator = request.GET.get("elevator")
        not_finished = request.GET.get("not_finished")
    
        filter_args = {}
        filter_args["realtor_id"] = int(realtor_id)
        if guest_phone:
            filter_args["guest_phone__contains"] = guest_phone
        if area_m2:
            filter_args["area_m2__gte"] = area_m2
        if deposit:
            filter_args["deposit__lte"] = deposit
        if month_fee:
            filter_args["month_fee__lte"] = month_fee
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
            lists = customers_models.ShopLeaseCustomer.objects.filter(**filter_args)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.CustomerStoreLeaseSerializer(lists, many=True, context={"request":request})
        return Response(serializer.data)

"""Customer Store Lease Finish"""