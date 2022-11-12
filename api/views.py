from django.shortcuts import render
from.models import Category,Post,Comment,UserModel
from.serializers import CategorySerializer,PostSerializer,CommentSerializer,UserModelSerializer
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

class UserModelviewset(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = "username"



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
