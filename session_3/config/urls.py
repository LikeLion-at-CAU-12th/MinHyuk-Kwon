"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from posts.views import *

# swagger 관련 부분
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info( # api 명세 작성하는 것을 도와주는 역할
        title = "LIKELION_KMH", # API 문서 타이틀
        default_version="1.0.0", # API 문서 버전
        description="KMH's first swagger api" # API 문서 설명
    ),
    public=True, # 인증 없이 누구나 문서 확인 가능
    permission_classes=(AllowAny,), # 접근 권한 설정
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/',include('posts.urls')),

    # swagger 관련 url
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('account/',include('accounts.urls')),
]

