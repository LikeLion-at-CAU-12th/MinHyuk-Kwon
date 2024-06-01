from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    # 이 필드들에 대해서는 required=True를 설정해주기 위해서 넣은 코드!
    class Meta:
        model = User
        fields = ['password', 'username', 'email']
    ### 여기까지는 7주차 DRF에서 한거랑 똑같은 듯

    def save(self, request):
        user = User.objects.create(
            username = self.validated_data['username'],
            email=self.validated_data['email'],
        )
        
        user.set_password(self.validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        email = data.get('email',None)
        # email = data['email']이라고 하지 않는 이유 -> keyError 방지

        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError('email already exists')
        return data

class AuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']
    
    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        user = User.get_user_or_none_by_username(username = username)

        if user is None:
            raise serializers.ValidationError("user account not exist")
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError("wrong password")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user" : user,
            "refresh_token" : refresh_token,
            "access_token" : access_token,
        }

        return data

class OAuthSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, data):
        email = data.get("email", None)
        
        user = User.get_user_or_none_by_email(email=email)
        
        if user is None:
            raise serializers.ValidationError("user account not exists")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data