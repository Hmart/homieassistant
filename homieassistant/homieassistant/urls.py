"""homieassistant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import os

from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import authentication, permissions

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
]

# OpenAPI docs
if os.getenv("ENV") in ("LOCAL", "DEV"):
    schema_view = get_schema_view(
        openapi.Info(title="API", default_version="v1",),
        public=True,
        permission_classes=(permissions.IsAdminUser,),
        authentication_classes=(authentication.SessionAuthentication,),
    )

    urlpatterns.extend(
        [
            re_path(
                r"^swagger(?P<format>\.json|\.yaml)$",
                schema_view.without_ui(cache_timeout=None),
                name="schema-json",
            ),
            path(
                "swagger/",
                schema_view.with_ui("swagger", cache_timeout=None),
                name="schema-swagger-ui",
            ),
            path(
                "redoc/",
                schema_view.with_ui("redoc", cache_timeout=None),
                name="schema-redoc",
            ),
        ]
    )
