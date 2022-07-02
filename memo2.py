
    path("customer-apartment-lease/", views.CustomerApartmentLeaseView.as_view()),
    path("customer-apartment-lease-updating/<int:pk>/", views.CustomerApartmentLeaseUpdatingView.as_view()),
    path("customer-apartment-lease-deleting/<int:pk>/", views.CustomerApartmentLeaseDeletingView.as_view()),
    path("customer-apartment-lease-searching/", views.CustomerApartmentLeaseSearchingView.as_view()),

    path("customer-building-lease/", views.CustomerBuildingLeaseView.as_view()),
    path("customer-building-lease-updating/<int:pk>/", views.CustomerBuildingLeaseUpdatingView.as_view()),
    path("customer-building-lease-deleting/<int:pk>/", views.CustomerBuildingLeaseDeletingView.as_view()),
    path("customer-building-lease-searching/", views.CustomerBuildingLeaseSearchingView.as_view()),

    path("customer-villa-lease/", views.CustomerVillaLeaseView.as_view()),
    path("customer-villa-lease-updating/<int:pk>/", views.CustomerVillaLeaseUpdatingView.as_view()),
    path("customer-villa-lease-deleting/<int:pk>/", views.CustomerVillaLeaseDeletingView.as_view()),
    path("customer-villa-lease-searching/", views.CustomerVillaLeaseSearchingView.as_view()),

    path("customer-officetel-lease/", views.CustomerOfficetelLeaseView.as_view()),
    path("customer-officetel-lease-updating/<int:pk>/", views.CustomerOfficetelLeaseUpdatingView.as_view()),
    path("customer-officetel-lease-deleting/<int:pk>/", views.CustomerOfficetelLeaseDeletingView.as_view()),
    path("customer-officetel-lease-searching/", views.CustomerOfficetelLeaseSearchingView.as_view()),

    path("customer-store-lease/", views.CustomerStoreLeaseView.as_view()),
    path("customer-store-lease-updating/<int:pk>/", views.CustomerStoreLeaseUpdatingView.as_view()),
    path("customer-store-lease-deleting/<int:pk>/", views.CustomerStoreLeaseDeletingView.as_view()),
    path("customer-store-lease-searching/", views.CustomerStoreLeaseSearchingView.as_view()),
