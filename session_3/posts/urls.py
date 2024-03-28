from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('introduction/', introduction, name = 'introduction'),
    path('page/', codeReview, name='codeReview'),
]