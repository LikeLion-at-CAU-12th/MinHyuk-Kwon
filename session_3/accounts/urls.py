from django.urls import path
from .views import *
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    #회원가입, 로그인, 로그아웃
    path("join/",RegisterView.as_view()),
    path("login/", AuthView.as_view()),
    path("logout/", LogoutView.as_view()),
    #탈퇴, 재가입
    path("withdraw/",WithdrawView.as_view()),
    path("rejoin/",RejoinView.as_view()),
    #토큰
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/varify/", TokenVerifyView.as_view()),
    #google OAuth
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
]