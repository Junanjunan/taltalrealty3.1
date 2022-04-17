from django.urls import path
from . import views

app_name = "customers"

urlpatterns = [
    path("houselease/", views.HouseLeaseCustomerList.as_view(), name="house-lease-customer-list"),
    path("houselease/<int:pk>/", views.HouseLeaseCustomerDeatil.as_view(), name="house-lease-customer-detail"),
    path("houselease/creating/", views.HouseLeaseCustomerCreating.as_view(), name="house-lease-customer-creating"),
    path("houselease/<int:pk>/update/", views.HouseLeaseCustomerUpdate.as_view(), name="house-lease-customer-update"),
    path("houselease/search/", views.houselease_customer_search, name="house-lease-customer-search"),
    path("houselease/<int:pk>/delete/", views.houselease_customer_delete, name="house-lease-customer-delete"),
    
    path("apartmentlease/", views.ApartmentLeaseCustomerList.as_view(), name="apartment-lease-customer-list"),
    path("apartmentlease/<int:pk>/", views.ApartmentLeaseCustomerDeatil.as_view(), name="apartment-lease-customer-detail"),
    path("apartmentlease/creating/", views.ApartmentLeaseCustomerCreating.as_view(), name="apartment-lease-customer-creating"),
    path("apartmentlease/<int:pk>/update/", views.ApartmentLeaseCustomerUpdate.as_view(), name="apartment-lease-customer-update"),
    path("apartmentlease/search/", views.apartmentlease_customer_search, name="apartment-lease-customer-search"),
    path("apartmentlease/<int:pk>/delete/", views.apartmentlease_customer_delete, name="apartment-lease-customer-delete"),

    path("officetellease/", views.OfficetelLeaseCustomerList.as_view(), name="officetel-lease-customer-list"),
    path("officetellease/<int:pk>/", views.OfficetelLeaseCustomerDeatil.as_view(), name="officetel-lease-customer-detail"),
    path("officetellease/creating/", views.OfficetelLeaseCustomerCreating.as_view(), name="officetel-lease-customer-creating"),
    path("officetellease/<int:pk>/update/", views.OfficetelLeaseCustomerUpdate.as_view(), name="officetel-lease-customer-update"),
    path("officetellease/search/", views.officetellease_customer_search, name="officetel-lease-customer-search"),
    path("officetellease/<int:pk>/delete/", views.officetellease_customer_delete, name="officetel-lease-customer-delete"),
    

    path("shoplease/", views.ShopLeaseCustomerList.as_view(), name="shop-lease-customer-list"),
    path("shoplease/<int:pk>/", views.ShopLeaseCustomerDeatil.as_view(), name="shop-lease-customer-detail"),
    path("shoplease/creating/", views.ShopLeaseCustomerCreating.as_view(), name="shop-lease-customer-creating"),
    path("shoplease/<int:pk>/update/", views.ShopLeaseCustomerUpdate.as_view(), name="shop-lease-customer-update"),
    path("shoplease/search/", views.shoplease_customer_search, name="shop-lease-customer-search"),
    path("shoplease/<int:pk>/delete/", views.shoplease_customer_delete, name="shop-lease-customer-delete"),
    
    path("housedealing/", views.HouseDealingCustomerList.as_view(), name="house-dealing-customer-list"),
    path("housedealing/<int:pk>/", views.HouseDealingCustomerDeatil.as_view(), name="house-dealing-customer-detail"),
    path("housedealing/creating/", views.HouseDealingCustomerCreating.as_view(), name="house-dealing-customer-creating"),
    path("housedealing/<int:pk>/update/", views.HouseDealingCustomerUpdate.as_view(), name="house-dealing-customer-update"),
    path("housedealing/search/", views.housedealing_customer_search, name="house-dealing-customer-search"),
    path("housedealing/<int:pk>/delete/", views.housedealing_customer_delete, name="house-dealing-customer-delete"),
    
    path("apartmentdealing/", views.ApartmentDealingCustomerList.as_view(), name="apartment-dealing-customer-list"),
    path("apartmentdealing/<int:pk>/", views.ApartmentDealingCustomerDeatil.as_view(), name="apartment-dealing-customer-detail"),
    path("apartmentdealing/creating/", views.ApartmentDealingCustomerCreating.as_view(), name="apartment-dealing-customer-creating"),
    path("apartmentdealing/<int:pk>/update/", views.ApartmentDealingCustomerUpdate.as_view(), name="apartment-dealing-customer-update"),
    path("apartmentdealing/search/", views.apartmentdealing_customer_search, name="apartment-dealing-customer-search"),
    path("apartmentdealing/<int:pk>/delete/", views.apartmentdealing_customer_delete, name="apartment-dealing-customer-delete"),

    path("officeteldealing/", views.OfficetelDealingCustomerList.as_view(), name="officetel-dealing-customer-list"),
    path("officeteldealing/<int:pk>/", views.OfficetelDealingCustomerDeatil.as_view(), name="officetel-dealing-customer-detail"),
    path("officeteldealing/creating/", views.OfficetelDealingCustomerCreating.as_view(), name="officetel-dealing-customer-creating"),
    path("officeteldealing/<int:pk>/update/", views.OfficetelDealingCustomerUpdate.as_view(), name="officetel-dealing-customer-update"),
    path("officeteldealing/search/", views.officeteldealing_customer_search, name="officetel-dealing-customer-search"),
    path("officeteldealing/<int:pk>/delete/", views.officeteldealing_customer_delete, name="officetel-dealing-customer-delete"),
    
    path("shopdealing/", views.ShopDealingCustomerList.as_view(), name="shop-dealing-customer-list"),
    path("shopdealing/<int:pk>/", views.ShopDealingCustomerDeatil.as_view(), name="shop-dealing-customer-detail"),
    path("shopdealing/creating/", views.ShopDealingCustomerCreating.as_view(), name="shop-dealing-customer-creating"),
    path("shopdealing/<int:pk>/update/", views.ShopDealingCustomerUpdate.as_view(), name="shop-dealing-customer-update"),
    path("shopdealing/search/", views.shopdealing_customer_search, name="shop-dealing-customer-search"),
    path("shopdealing/<int:pk>/delete/", views.shopdealing_customer_delete, name="shop-dealing-customer-delete"),

    path("buildingdealing/", views.BuildingDealingCustomerList.as_view(), name="building-dealing-customer-list"),
    path("buildingdealing/<int:pk>/", views.BuildingDealingCustomerDeatil.as_view(), name="building-dealing-customer-detail"),
    path("buildingdealing/creating/", views.BuildingDealingCustomerCreating.as_view(), name="building-dealing-customer-creating"),
    path("buildingdealing/<int:pk>/update/", views.BuildingDealingCustomerUpdate.as_view(), name="building-dealing-customer-update"),
    path("buildingdealing/search/", views.buildingdealing_customer_search, name="building-dealing-customer-search"),
    path("buildingdealing/<int:pk>/delete/", views.buildingdealing_customer_delete, name="building-dealing-customer-delete"),
]