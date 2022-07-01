path("customer-officetel-dealing/", views.CustomerOfficetelDealingView.as_view()),
    path("customer-officetel-dealing-updating/<int:pk>/", views.CustomerOfficetelDealingUpdatingView.as_view()),
    path("customer-officetel-dealing-deleting/<int:pk>/", views.CustomerOfficetelDealingDeletingView.as_view()),
    path("customer-officetel-dealing-searching/", views.CustomerOfficetelDealingSearchingView.as_view()),