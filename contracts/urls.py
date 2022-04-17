from django.urls import path
from . import views

app_name = "contracts"

urlpatterns = [
    path("", views.ContractsList.as_view(), name="list"),
    path("creating/", views.ContractCreating.as_view(), name="creating"),
    path("<int:pk>/", views.ContractDetail.as_view(), name="detail"),
    path("update/<int:pk>/", views.ContractUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.contract_delete, name="delete")
]
