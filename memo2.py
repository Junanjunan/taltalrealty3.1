path("customer-apartment-dealing/", views.CustomerApartmentDealingView.as_view()),
path("customer-apartment-dealing-updating/<int:pk>/", views.CustomerApartmentDealingUpdatingView.as_view()),
path("customer-apartment-dealing-deleting/<int:pk>/", views.CustomerApartmentDealingDeletingView.as_view()),
path("customer-apartment-dealing-searching/", views.CustomerApartmentDealingSearchingView.as_view()),
