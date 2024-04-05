from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from posts.models import *
#from .models import CodeReviewer  3주차 챌린지 과제용

# Create your views here.
def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello lielion-12th!"
        })
        
def introduction(request):
    if request.method == "GET":
        return JsonResponse({
	'status' : 200,
	'success' : True,
	'message' : '메시지 전달 성공!',
	'data' : [
		{
			"name" : "권민혁",
			"age" : 25,
			"major" : "Economics"
		},
		{
			"name" : "박예빈",
			"age" : 25,
			"major" : "chemical_engineering"
		}
	]
})

@require_http_methods(["GET"])
def get_post_detail(request, id):
	post = get_object_or_404(Post, pk=id)
	post_detail_json = {
		"id" : post.id,
		"title" : post.title,
		"content" : post.content,
		"writer" : post.writer,
		"category" : post.category
	}

	return JsonResponse({
		"status" : 200,
		"message" : "게시글 조회 성공",
		"data" : post_detail_json
	})

# 3주차 챌린지 과제
# def codeReview(request):
# 	if request.method == "GET":
# 		# model에 나와 코드리뷰어의 데이터 생성하기 -> shell 환경에서 진행함
# 		#CodeReviewer.objects.create(name = "권민혁", age = 25, major = "Economics", gitHub = "@kmh0601")
# 		#CodeReviewer.objects.create(name = "박예빈", age = 25, major = "Chemical_engineering", gitHub = "@yebinnnnn")
		
# 		# CodeReviewer 모델 사용하기
# 		codeReviewer = CodeReviewer.objects.filter()
# 		# return render 매개변수에 모델 추가하기
# 		return render(request, 'challenge.html', {'codeReviewer': codeReviewer})
