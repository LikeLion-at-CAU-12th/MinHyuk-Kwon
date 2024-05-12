from rest_framework import permissions

KEY = "LIKELION12"

# header에 key를 제대로 입력한 유저인지
class KeyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 인증된 유저인 경우
        if request.user.is_authenticated:
            # 헤더의 key값이 내가 정한 key와 같은지 확인!
            if request.META['HTTP_KEY'] == KEY:
                return True
        return False

# KeyPermission은 모든 api 요청에 대해 기본적으로 수행되므로 이를 상속한다
class IsAuthorOrReadOnly(KeyPermission):
    def has_object_permission(self, request, view, obj):
        # 요청이 GET, OPTIONS, HEAD인 경우
        if request.method in permissions.SAFE_METHODS:
            return True
        # 요청한 user와 post의 user가 같다면 수정/삭제 허용
        elif request.user.id == obj.user.id:
            return True
        return False