from django.contrib import admin
from import_export.admin import ExportActionModelAdmin, ImportExportMixin, ImportMixin, ImportExportModelAdmin
from . import models

# @admin.register(resources.BaseItems)
# class BaseItemsAdmin(ImportExportModelAdmin):
#     resources_class = resources.BaseItemsAdminResource

# @admin.register(models.AdItems)
# class AdItemsAdmin(admin.ModelAdmin):
#     pass

# @admin.register(models.BaseItems)
# class BaseItemsAdmin(admin.ModelAdmin):
#     pass

# @admin.register(models.CommonItems)
# class CommonItemsAdmin(admin.ModelAdmin):
#     pass

# @admin.register(models.DealingItems)
# class DealingItemsAdmin(admin.ModelAdmin):
#     pass

# @admin.register(models.RoomItems)
# class RoomItemsAdmin(admin.ModelAdmin):
#     pass

@admin.register(models.ApartmentDealing)
class AparmentDealingAdmin(ImportExportMixin, admin.ModelAdmin):

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
class RoomDealingAdmin(ImportExportMixin, admin.ModelAdmin):

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
class OfficetelDealingAdmin(ImportExportMixin, admin.ModelAdmin):

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
class StoreDealingAdmin(ImportExportMixin, admin.ModelAdmin):

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
class BuildingDealingAdmin(ImportExportMixin, admin.ModelAdmin):

    list_display = (
        "address",
        "realtor",
        "realtor_id",
        "updated",
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
class ApartmentLeaseAdmin(ImportExportMixin, admin.ModelAdmin):

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
class RoomLeaseAdmin(ImportExportMixin, admin.ModelAdmin):

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
class OfficetelLeaseAdmin(ImportExportMixin, admin.ModelAdmin):

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
class StoreLeaseAdmin(ImportExportMixin, admin.ModelAdmin):

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