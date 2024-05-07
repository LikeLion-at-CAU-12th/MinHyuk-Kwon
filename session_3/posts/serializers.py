from rest_framework import serializers
from .models import Post
from .models import Comment
from django.core.exceptions import ValidationError 

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

        # # 원하는 필드만 가져올 수 있음
        # fileds = ['writer','content'] 
        # # 원하지 않는 필드를 지정할 수 있음
        # exclude = ['category'] 
        # # 수정 불가능 옵션으로 필드를 가져올 수 있음
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        # exclude = ['post']
    
    # def validat_post(self, value):
    #     return value
		
    # def validate(self, data):
    #     print('hi')
    #     if data['title'] == '':
    #         return ValidationError('required title field')
    #     elif data['writer'] == '':
    #         return ValidationError('required writer field')
    #     return data
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        # post 필드의 유효성 검사 함수를 제거합니다.
            self.fields['post'].validators = []