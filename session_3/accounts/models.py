from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass #해당 세션에서 바로 유저모델을 사용할 것은 아니기 때문에 pass로 넣겠습니다.

    @staticmethod
    def get_user_or_none_by_username(username):
        # 왜 try-exception? -> get은 error를 반환! filter는 None을 반환~
        try:
            return User.objects.get(username=username)
        except Exception:
            return None
        