from django.contrib import admin
from . import models

@admin.register(models.ApartmentDealingCustomer)
class ApartmentDealingCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "room",
        "area_m2",
        "parking",
        "elevator",
        "loan",
        "not_finished",
        "description",
    )


@admin.register(models.HouseDealingCustomer)
class HouseDealingCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "room",
        "area_m2",
        "parking",
        "elevator",
        "loan",
        "not_finished",
        "description",
    )


@admin.register(models.OfficetelDealingCustomer)
class OfficetelDealingCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "room",
        "area_m2",
        "parking",
        "elevator",
        "loan",
        "not_finished",
        "description",
    )



@admin.register(models.ShopDealingCustomer)
class ShopDealingCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "area_m2",
        "parking",
        "elevator",
        "loan",
        "not_finished",
        "description",
    )


@admin.register(models.BuildingDealingCustomer)
class BuildingDealingCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "land_m2",
        "elevator",
        "not_finished",
        "description",
    )


@admin.register(models.ApartmentLeaseCustomer)
class ApartmentLeaseCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "deposit",
        "month_fee",
        "room",
        "area_m2",
        "parking",
        "elevator",
        "loan",
        "loan",
        "not_finished",
        "description",
    )


@admin.register(models.HouseLeaseCustomer)
class HouseLeaseCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "deposit",
        "month_fee",
        "room",
        "area_m2",
        "parking",
        "elevator",
        "loan",
        "loan",
        "not_finished",
        "description",
    )


@admin.register(models.OfficetelLeaseCustomer)
class OfficetelLeaseCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "deposit",
        "month_fee",
        "room",
        "area_m2",
        "parking",
        "elevator",
        "loan",
        "loan",
        "not_finished",
        "description",
    )


@admin.register(models.ShopLeaseCustomer)
class ShopLeaseCustomerAdmin(admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "deposit",
        "month_fee",
        "area_m2",
        "parking",
        "elevator",
        "loan",
        "not_finished",
        "description",
    )





