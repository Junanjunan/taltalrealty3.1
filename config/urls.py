"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("users/", include('users.urls', namespace='users')),
    path("books/", include('books.urls', namespace='books')),
    path("customers/", include('customers.urls', namespace='customers')),
    path("contracts/", include('contracts.urls', namespace="contracts")),
    path("managements/", include('managements.urls', namespace="managements")),
    path("api/v1/", include('apis.urls', namespace='api')),
    path('admin/', admin.site.urls),
    path('sentry-debug/', trigger_error),
    # path('verification/', include('verify_email.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
