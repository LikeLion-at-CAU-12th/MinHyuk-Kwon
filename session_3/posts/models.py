from django.db import models

# Create your models here.

# class CodeReviewer(models.Model):
#     name = models.CharField(max_length=5)
#     age = models.IntegerField()
#     major = models.CharField(max_length=20)
#     gitHub = models.CharField(max_length=20)


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta():
        abstract = True

class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),  # db에 저장할 실제 값, 우리 눈에 보이는 값
        ('STUDY', '공부'),
        ('ETC', '기타')
    )
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='제목', max_length=20)
    content = models.TextField(verbose_name='내용')
    writer = models.CharField(verbose_name='작성자', max_length=10)
    category = models.CharField(choices=CHOICES, max_length=20)