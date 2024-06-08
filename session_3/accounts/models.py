from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    pass #해당 세션에서 바로 유저모델을 사용할 것은 아니기 때문에 pass로 넣겠습니다.

    # 삭제 여부 및 삭제 일시 필드 추가
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # soft delete
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    # 재가입
    def rejoin(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()


    @staticmethod
    def get_user_or_none_by_username(username):
        # 왜 try-exception? -> get은 error를 반환! filter는 None을 반환~
        try:
            return User.objects.get(username=username)
        except Exception:
            return None

    # 얘가 추가된게 중요하다고 하네요~
    @staticmethod
    def get_user_or_none_by_email(email):
        try:
            return User.objects.get(email=email)
        except Exception:
            return None

    