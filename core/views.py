from django.http import JsonResponse
from django.shortcuts import render

# third party imports
from rest_framework import (viewsets,
                            permissions,
                            mixins,
                            generics
                            )
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# from rest_framework.views import APIView

from .serializers import PostSerializer, UserSerializer
from blog.models import Post
from django.contrib.auth.models import User


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )




class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostCreateView(mixins.ListModelMixin, generics.CreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# class PostView(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):
#     serializer_class = PostSerializer
#     queryset = Post.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class TestView(APIView):
#     permission_classes = (IsAuthenticated, )
#
#     def get(self, request, *args, **kwargs):
#         qs = Post.published.all()
#         serializer = PostSerializer(qs, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save() # can save only is is valid!
#             return Response(serializer.data)
#         return Response(serializer.errors)

# def test_view(request):
#     data = {
#         'name': 'Mike',
#         'age': 22
#     }
#     return JsonResponse(data) #safe=False if you want to pass a list
