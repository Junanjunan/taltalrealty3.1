from django.urls import path
from homes import views as home_views

app_name = "core"

urlpatterns = [
    path("", home_views.homes, name='home'),
    path("privacy/", home_views.privacy, name="privacy")
]