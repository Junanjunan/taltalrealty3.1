from django.urls import path
from . import views

app_name = "managements"

urlpatterns = [
    path("", views.ManagementList.as_view(), name="list"),
    path("creating/", views.ManagementCreating.as_view(), name="creating"),
    path("update/<int:pk>/", views.ManagementUpdate.as_view(), name="update"),
    path("<int:pk>/", views.ManagementDetail.as_view(), name="detail"),
    path("<int:pk>/delete/", views.management_delete, name="delete"),
    path("mailing/", views.ManagementMailing.as_view(), name="mailing")
]
