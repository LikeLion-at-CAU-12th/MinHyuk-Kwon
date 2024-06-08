from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.shortcuts import get_list_or_404
from django.views.decorators.http import require_http_methods
from posts.models import *
#from .models import CodeReviewer  3주차 챌린지 과제용
import json
from datetime import datetime, timedelta

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

# 5주차 과제1
@require_http_methods(["POST","GET"])
def comment_list(request, post_id):
	if request.method == "POST":
		body = json.loads(request.body.decode("utf-8"))

		new_comment = Comment.objects.create(
			post_id = post_id,
			writer = body['writer'],
			comment = body['comment']
		)

		new_comment_json = {
			"post_id" : new_comment.post_id,
			"comment" : new_comment.comment,
			"writer" : new_comment.writer
		}

		return JsonResponse({
			"status" : 200,
			"message" : "새로운 댓글 작성 완료",
			"data" : new_comment_json
		})

	elif request.method == "GET":
		# comment_all = Comment.objects.filter(post_id = post_id)
		comment_all = get_list_or_404(Comment, post_id = post_id)
		comment_json_all = []

		for comment in comment_all:
			comment_json = {
				"id" : comment.id,
				"comment" : comment.comment,
				"writer" : comment.writer
			}
			comment_json_all.append(comment_json)

		return JsonResponse({
			"status" : 200,
			"message" : f"{post_id}번 게시글의 모든 댓글",
			"data" : comment_json_all
		})

# 5주차 과제2
@require_http_methods(["GET"])
def post_made_week(request):
	post_list = get_list_or_404(Post.objects.order_by('created_at'), created_at__range = [datetime.now() - timedelta(days=7), datetime.now()])
	#post_list = Post.objects.filter(created_at__range = [date.today() - timedelta(days=7), date.today()])
	#post_list = Post.objects.filter(created_at__range = [datetime.now() - timedelta(days=7), datetime.now()])

	post_json_list = []
	for post in post_list:
		post_json = {
			"id" : post.id,
			"writer" : post.writer,
			"title" : post.title,
			"content" : post.content,
			"category" : post.category,
			"created_at" : post.created_at
		}
		post_json_list.append(post_json)
	
	return JsonResponse({
		"state" : 200,
		"message" : "최근 일주일간 생성된 포스트 조회 성공",
		"data" : post_json_list,
		"now" : datetime.now()
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


# 7th session
# 위에서 작성한 긴 api를 class base view로 간결하게 작성함

from .serializers import PostSerializer
from .serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import generics

# class PostList(APIView):
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save();
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many = True)
#         return Response(serializer.data)
	
# class PostDetail(APIView):
# 	def get(self, request, id):
# 		post=  get_object_or_404(Post,id=id)
# 		serializer = PostSerializer(post)
# 		return Response(serializer.data)
from config.permissions import *

class PostList(APIView):
	# 인가 추가!
    permission_classes = [KeyPermission]

    def post(self, request, format=None):
        data = request.data
        data['user'] = request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid(data):
            serializer.save();
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data)

from rest_framework.permissions import IsAuthenticatedOrReadOnly
class PostDetail(APIView):
	# 인가 추가!
	permission_classes = [IsAuthorOrReadOnly]

	def get(self, request, id):
		post=  get_object_or_404(Post,id=id)
		serializer = PostSerializer(post)
		return Response(serializer.data)
	
# 	def put(self, request, id):
# 		post = get_object_or_404(Post,id=id)
# 		serializer = PostSerializer(post, data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_200_OK)
# 		return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

# 	def delete(self, request, id):
# 		post = get_object_or_404(Post, id=id)
# 		post.delete()
# 		return Response(status=status.HTTP_204_NO_CONTENT)

from config import S3ImageUploader

class PostList(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def post(self, request, format=None):
		data = request.data
		print(data)
		serializer = PostSerializer(data=data)
		if serializer.is_valid():
			image = request.FILES["thumbnail"]
			url = S3ImageUploader.S3ImageUploader(image).upload()
			serializer.save(thumbnail = url);
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	lookup_field = 'id'

class CommentList(generics.ListCreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	lookup_field = 'post_id'

	# perform_create는 serializer를 인자로 받아 serializer.save()를 실행하는 함수!
	# def perform_create(self, serializer):
	# 	serializer.save(post_id = self.kwargs.get('id'))
	def create(self, request, *args, **kwargs):
		request_data = request.data.copy()  # 요청 데이터 복사
		request_data['post'] = kwargs.get('id')  # 'post_id' 값을 추가
		serializer = self.get_serializer(data=request_data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

### CBV : APIVIEW
# class CommentList(APIView):
# 	def post(self, request, id):
# 		serializer = CommentSerializer(data = request.data)
# 		if serializer.is_valid():
# 			serializer.save(post_id = id)
# 			return Response(serializer.data, status=status.HTTP_200_OK)
# 		return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
	
# 	# 특정 게시글의 모든 댓글 가져오기
# 	def get(self, request, id):
# 		comments = get_list_or_404(Comment, post_id = id)
# 		serializer = CommentSerializer(comments, many = True)
# 		return Response(serializer.data, status=status.HTTP_200_OK)
	def delete(self, request, id):
		post = get_object_or_404(Post, id=id)
		self.check_object_permissions(self.request, post)
		post.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
	def post(self, request, id):
		data = request.data
		data['post'] = id
		serializer = CommentSerializer(data = data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
	
	# 특정 게시글의 모든 댓글 가져오기
	def get(self, request, id):
		comments = get_list_or_404(Comment, post_id = id)
		serializer = CommentSerializer(comments, many = True)
		return Response(serializer.data, status=status.HTTP_200_OK)
