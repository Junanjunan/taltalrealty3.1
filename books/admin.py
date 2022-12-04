from django.contrib import admin
from . import models


@admin.register(models.ApartmentDealing)
class AparmentDealingAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "deposit",
        "month_fee",
        "management_fee",
        "room",
        "bath",
        "area_m2",
        "total_area_m2",
        "land_m2",
        "birth",
        "parking",
        "elevator",
        "empty",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )


@admin.register(models.RoomDealing)
class RoomDealingAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "deposit",
        "month_fee",
        "management_fee",
        "room",
        "bath",
        "area_m2",
        "total_area_m2",
        "land_m2",
        "birth",
        "parking",
        "elevator",
        "empty",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )


@admin.register(models.OfficetelDealing)
class OfficetelDealingAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "deposit",
        "month_fee",
        "management_fee",
        "room",
        "bath",
        "area_m2",
        "total_area_m2",
        "land_m2",
        "birth",
        "parking",
        "elevator",
        "empty",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )


@admin.register(models.StoreDealing)
class StoreDealingAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "deposit",
        "month_fee",
        "management_fee",
        "bath",
        "area_m2",
        "total_area_m2",
        "land_m2",
        "birth",
        "parking",
        "elevator",
        "empty",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )


@admin.register(models.BuildingDealing)
class BuildingDealingAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "room",
        "bath",
        "price",
        "deposit",
        "month_fee",
        "management_fee",
        "birth",
        "floor_top",
        "floor_bottom",
        "land_type",
        "land_m2",
        "building_area_m2",
        "total_floor_area_m2",
        "total_floor_area_m2_for_ratio",
        "building_coverage",
        "floor_area_ratio",
        "parking_number",
        "elevator",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )


@admin.register(models.ApartmentLease)
class ApartmentLeaseAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "deposit",
        "month_fee",
        "management_fee",
        "room",
        "bath",
        "area_m2",
        "total_area_m2",
        "land_m2",
        "birth",
        "parking",
        "elevator",
        "empty",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )


@admin.register(models.RoomLease)
class RoomLeaseAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "deposit",
        "month_fee",
        "management_fee",
        "room",
        "bath",
        "area_m2",
        "total_area_m2",
        "land_m2",
        "birth",
        "parking",
        "elevator",
        "empty",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )


@admin.register(models.OfficetelLease)
class OfficetelLeaseAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "deposit",
        "month_fee",
        "management_fee",
        "room",
        "bath",
        "area_m2",
        "total_area_m2",
        "land_m2",
        "birth",
        "parking",
        "elevator",
        "empty",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )


@admin.register(models.StoreLease)
class StoreLeaseAdmin(admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
        "right_deposit",
        "deposit",
        "month_fee",
        "management_fee",
        "bath",
        "area_m2",
        "total_area_m2",
        "land_m2",
        "birth",
        "parking",
        "elevator",
        "empty",
        "loan",
        "not_finished",
        "naver",
        "dabang",
        "zicbang",
        "peterpan",
        "owner_phone",
        "tenant_phone",
        "description",        
    )