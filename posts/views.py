#import json 
#from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post, Comment
from django.contrib.auth.models import User
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPostAuthor
from rest_framework.authentication import TokenAuthentication
from django.http import Http404

if not User.objects.filter(username="new_user").exists():
    user = User.objects.create_user(username="new_user", password="secure_pass123")
    print(f"User '{user.username}' created successfully.")
else:
    print("User already exists.")

user = authenticate(username="new_user", password="secure_pass123")
if user is not None:
    print("Authentication successful!")
else:
    print("Invalid credentials.")

admin_group, created = Group.objects.get_or_create(name="Admin")  # ✅ Ensures the group exists

try:
    user = User.objects.get(username="admin_user")  # ✅ Only fetch if user exists
    user.groups.add(admin_group)
except User.DoesNotExist:
    print("Error: User 'admin_user' does not exist. Please create this user first.")

class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]  

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404  

    def get(self, request, pk):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})

    def delete(self, request, pk):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        print("Headers Received:", request.headers)  
        return Response({"message": "Authenticated!"})


class UserListCreate(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListCreate(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentListCreate(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#def get_users(request):
#    try:
#        users = list(User.objects.values('id', 'username', 'email', 'created_at'))
#        return JsonResponse(users, safe=False)
#    except Exception as e:
#        return JsonResponse({'error': str(e)}, status=500)
    
#@csrf_exempt 
#def create_user(request): 
#       if request.method == 'POST': 
#            try: 
#                data = json.loads(request.body)
#                user = User.objects.create(username=data['username'], email=data['email'])
#                return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status=201) 
#            except Exception as e: 
#                return JsonResponse({'error': str(e)}, status=400)
            
#@csrf_exempt 
#def update_user(request, id):
#        if request.method == 'PUT': 
#            try: 
#                data = json.loads(request.body) 
#                email = data['email']
#                user = User.objects.filter(id=id).first()
#                # data = UserSerializer(isinstance=user, data=request.data) 
#                user.email = email 
#                user.save() 
#               return JsonResponse({'message': 'User updated successfully'}, status=201) 
#            except Exception as e: 
#                return JsonResponse({'error': str(e)}, status=400)
        
#@csrf_exempt 
#def delete_user(request, id): 
#        if request.method == 'DELETE':
#             try: 
#                user = User.objects.filter(id=id).first() 
#                user.delete() #User.objects.delete(id=id) 
#                return JsonResponse({'message': 'User deleted successfully'}, status=200) 
#             except Exception as e: 
#                 return JsonResponse({'error': str(e)}, status=400)