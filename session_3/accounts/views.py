from django.shortcuts import render
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout

class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user" : serializer.data,
                    "message" : "register success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthView(APIView):
    def post(self,request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            res = Response(
                {
                    "user" : {
                        "id" : user.id,
                        "email" : user.email,
                    },
                    "message" : "login success",
                    "token" : {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access_token", access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_200_OK)


class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializers = DeleteAndRejoinSerializer(data = request.data)
        if serializers.is_valid(raise_exception=True):
            user = serializers.validated_data["user"]
            # 이게 model에 작성한 내부 함수를 이용한다는 의도이긴 한데 과제의 의도와 맞는지는 애매....
            user.soft_delete()
            return Response({"message" : "탈퇴 완료", "deleted_at : " : user.deleted_at }, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class RejoinView(APIView):
    
    def post(self, request):
        serializers = DeleteAndRejoinSerializer(data = request.data)
        # 다시 생각해보니 rejoin은 validation에 is_deleted == True인지 확인하는 부분 + 탈퇴한지 일주일 이내인지 확인이 필요한듯! 그냥 serializer를 분리하자 ㅠㅠ 
        if serializers.is_valid(raise_exception=True):
            user = serializers.validated_data["user"]
            user.rejoin()
            return Response({"message" : "재가입 완료"}, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        
from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

GOOGLE_SCOPE_USERINFO = get_secret("GOOGLE_SCOPE_USERINFO")
GOOGLE_REDIRECT = get_secret("GOOGLE_REDIRECT")
GOOGLE_CALLBACK_URI = get_secret("GOOGLE_CALLBACK_URI")
GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")
GOOGLE_SECRET = get_secret("GOOGLE_SECRET")

from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests

def google_login(request):
   scope = GOOGLE_SCOPE_USERINFO        # + "https://www.googleapis.com/auth/drive.readonly" 등 scope 설정 후 자율적으로 추가
   return redirect(f"{GOOGLE_REDIRECT}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    code = request.GET.get("code")      # Query String 으로 넘어옴
    
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)

    google_access_token = token_req_json.get('access_token')

    email_response = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={google_access_token}")
    res_status = email_response.status_code

    if res_status != 200:
        return JsonResponse({'status': 400,'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    email_res_json = email_response.json()
    # email = email_res_json.get('email')

    serializer = OAuthSerializer(data=email_res_json)
    try:
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            res = JsonResponse(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
    except:       # 회원가입이 필요함
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)