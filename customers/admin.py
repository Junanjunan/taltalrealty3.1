from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin
from . import models

@admin.register(models.ApartmentDealingCustomer)
class ApartmentDealingCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

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
        "not_finished",
        "description",
    )


@admin.register(models.HouseDealingCustomer)
class HouseDealingCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

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
        "not_finished",
        "description",
    )


@admin.register(models.OfficetelDealingCustomer)
class OfficetelDealingCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

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
        "not_finished",
        "description",
    )



@admin.register(models.ShopDealingCustomer)
class ShopDealingCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

    list_display = (
        "guest_phone",
        "realtor",
        "realtor_id",
        "updated",
        "price",
        "area_m2",
        "parking",
        "elevator",
        "not_finished",
        "description",
    )


@admin.register(models.BuildingDealingCustomer)
class BuildingDealingCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

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
class ApartmentLeaseCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

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
        "not_finished",
        "description",
    )


@admin.register(models.HouseLeaseCustomer)
class HouseLeaseCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

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
        "not_finished",
        "description",
    )


@admin.register(models.OfficetelLeaseCustomer)
class OfficetelLeaseCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

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
        "not_finished",
        "description",
    )


@admin.register(models.ShopLeaseCustomer)
class ShopLeaseCustomerAdmin(ImportExportMixin, admin.ModelAdmin):

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
        "not_finished",
        "description",
    )





