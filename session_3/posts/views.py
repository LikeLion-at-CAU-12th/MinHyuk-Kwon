from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from posts.models import *
#from .models import CodeReviewer  3주차 챌린지 과제용
import json

@require_http_methods(["POST", "GET"])
def post_list(request):

	if request.method == "POST":
		body = json.loads(request.body.decode("utf-8"))

		# 새로운 데이터를 DB에 생성
		new_post = Post.objects.create(
			writer = body['writer'],
			title = body['title'],
			content = body['content'],
			category = body['category']
		)

		# json으로 response 생성 (위에서 새로 생성된 데이터에 대한 정보를 담은 json)
		new_post_json = {
			"id" : new_post.id,
			"writer" : new_post.writer,
			"title" : new_post.title,
			"content" : new_post.content,
			"category" : new_post.category
		}

		# response 반환
		return JsonResponse({
			"status" : 200,
			"message" : "게시글 작성 성공",
			"data" : new_post_json
		})

	elif request.method == "GET":
		post_all = Post.objects.all()

		post_json_all = []

		for post in post_all:
			post_json = {
				"id" : post.id,
				"writer" : post.writer,
				"title" : post.title,
				"content" : post.content,
				"category" : post.category
			}
			post_json_all.append(post_json)
		
		return JsonResponse({
			"status" : 200,
			"message" : "게시글 목록 조회 성공",
			"data" : post_json_all
		})

@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):

	if request.method == "GET":
		post = get_object_or_404(Post, pk=id)

		post_json = {
			"id" : post.id,
			"writer" : post.writer,
			"title" : post.title,
			"content" : post.content,
			"category" : post.category
		}

		return JsonResponse({
			"status" : 200,
			"message" : "개별 조회 성공",
			"data" : post_json
		})

	elif request.method == "PATCH":

		body = json.loads(request.body.decode('utf-8'))

		update_post = get_object_or_404(Post, pk = id)

		update_post.title = body["title"]
		update_post.content = body["content"]
		update_post.category = body["category"]

		update_post.save()

		update_post_json = {
			"id" : update_post.id,
			"writer" : update_post.writer,
			"title" : update_post.title,
			"content" : update_post.content,
			"category" : update_post.category
		}

		return JsonResponse({
			"state" : 200,
			"message" : "게시글 수정 성공",
			"data" : update_post_json
		})
	elif request.method == "DELETE":
		delete_post = get_object_or_404(Post, pk = id)
		delete_post.delete()

		return JsonResponse({
			"status" : 200,
			"message" : "게시글 삭제 성공",
			"data" : None
		})


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
	post = get_object_or_404(Post, id=id)
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
