from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("me/", views.MeView.as_view()),
    path("test/", views.TestView.as_view()),
    path("users/login/", views.LoginView.as_view()),
    path("books-apartment-dealing/", views.BooksApartmentDealingView.as_view())
]
