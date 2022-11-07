from django.shortcuts import render
from.models import Category,Post,Comment
from.serializers import CategorySerializer,PostSerializer,CommentSerializer
from rest_framework import viewsets

# Create your views here.

class Categoryviewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class Postviewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

    

class Commentviewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
