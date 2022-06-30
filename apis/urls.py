from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("allUser/", views.AllUserView.as_view()),
    path("userToken/<int:pk>/", views.SocialLoginTokenView.as_view()),
    path("me/", views.MeView.as_view()),
    path("profile/<int:pk>/", views.ProfileView.as_view()),
    path("test/", views.TestView.as_view()),
    path("users/login/", views.LoginView.as_view()),
    # path("users/social-login/", views.SocialLoginView.as_view()),
    path("login/kakao/", views.kakao_login_app, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback_app),
    path("login/naver/", views.naver_login_app, name="naver-login"),
    path("login/naver/callback/", views.naver_callback_app),
    path("login/github/", views.github_login_app, name="github-login"),
    path("login/github/callback/", views.github_callback_app),
    path("users/social-logout/", views.social_logout),
    
    path("books-apartment-dealing/", views.BooksApartmentDealingView.as_view()),
    path("books-apartment-dealing/<int:pk>/", views.BooksApartmentDealingDetailView.as_view()),
    
    path("books-villa-dealing/", views.BooksVillaDealingView.as_view()),
    path("books-villa-dealing-updating/<int:pk>/", views.BooksVillaDealingUpdatingView.as_view()),
    path("books-villa-dealing-deleting/<int:pk>/", views.BooksVillaDealingDeletingView.as_view()),
    path("books-villa-dealing-searching/", views.BooksVillaDealingSearchingView.as_view()),
    
    path("books-apartment-dealing/", views.BooksApartmentDealingView.as_view()),
    path("books-apartment-dealing-updating/<int:pk>/", views.BooksApartmentDealingUpdatingView.as_view()),
    path("books-apartment-dealing-deleting/<int:pk>/", views.BooksApartmentDealingDeletingView.as_view()),
    path("books-apartment-dealing-searching/", views.BooksApartmentDealingSearchingView.as_view()),

    path("books-officetel-dealing/", views.BooksOfficetelDealingView.as_view()),
    path("books-officetel-dealing-updating/<int:pk>/", views.BooksOfficetelDealingUpdatingView.as_view()),
    path("books-officetel-dealing-deleting/<int:pk>/", views.BooksOfficetelDealingDeletingView.as_view()),
    path("books-officetel-dealing-searching/", views.BooksOfficetelDealingSearchingView.as_view()),

    path("books-store-dealing/", views.BooksStoreDealingView.as_view()),
    path("books-store-dealing-updating/<int:pk>/", views.BooksStoreDealingUpdatingView.as_view()),
    path("books-store-dealing-deleting/<int:pk>/", views.BooksStoreDealingDeletingView.as_view()),
    path("books-store-dealing-searching/", views.BooksStoreDealingSearchingView.as_view()),

    path("books-building-dealing/", views.BooksBuildingDealingView.as_view()),
    path("books-building-dealing-updating/<int:pk>/", views.BooksBuildingDealingUpdatingView.as_view()),
    path("books-building-dealing-deleting/<int:pk>/", views.BooksBuildingDealingDeletingView.as_view()),
    path("books-building-dealing-searching/", views.BooksBuildingDealingSearchingView.as_view()),

    path("books-villa-lease/", views.BooksVillaLeaseView.as_view()),
    path("books-villa-lease-updating/<int:pk>/", views.BooksVillaLeaseUpdatingView.as_view()),
    path("books-villa-lease-deleting/<int:pk>/", views.BooksVillaLeaseDeletingView.as_view()),
    path("books-villa-lease-searching/", views.BooksVillaLeaseSearchingView.as_view()),
    
    path("books-apartment-lease/", views.BooksApartmentLeaseView.as_view()),
    path("books-apartment-lease-updating/<int:pk>/", views.BooksApartmentLeaseUpdatingView.as_view()),
    path("books-apartment-lease-deleting/<int:pk>/", views.BooksApartmentLeaseDeletingView.as_view()),
    path("books-apartment-lease-searching/", views.BooksApartmentLeaseSearchingView.as_view()),

    path("books-officetel-lease/", views.BooksOfficetelLeaseView.as_view()),
    path("books-officetel-lease-updating/<int:pk>/", views.BooksOfficetelLeaseUpdatingView.as_view()),
    path("books-officetel-lease-deleting/<int:pk>/", views.BooksOfficetelLeaseDeletingView.as_view()),
    path("books-officetel-lease-searching/", views.BooksOfficetelLeaseSearchingView.as_view()),

    path("books-store-lease/", views.BooksStoreLeaseView.as_view()),
    path("books-store-lease-updating/<int:pk>/", views.BooksStoreLeaseUpdatingView.as_view()),
    path("books-store-lease-deleting/<int:pk>/", views.BooksStoreLeaseDeletingView.as_view()),
    path("books-store-lease-searching/", views.BooksStoreLeaseSearchingView.as_view()),

    path("customer-apartment-dealing/", views.CustomerApartmentDealingView.as_view()),
    path("customer-apartment-dealing-updating/<int:pk>/", views.CustomerApartmentDealingUpdatingView.as_view()),
    path("customer-apartment-dealing-deleting/<int:pk>/", views.CustomerApartmentDealingDeletingView.as_view()),
    path("customer-apartment-dealing-searching/", views.CustomerApartmentDealingSearchingView.as_view()),


    path("contracts/", views.ContractView.as_view()),
    path("contract-updating/<int:pk>/", views.ContractUpdatingView.as_view()),
    path("contract-deleting/<int:pk>/", views.ContractDeletingView.as_view()),
    
    path("managements/", views.ManagementView.as_view()),
    path("management-updating/<int:pk>/", views.ManagementUpdatingView.as_view()),
    path("management-deleting/<int:pk>/", views.ManagementDeletingView.as_view()),
]
