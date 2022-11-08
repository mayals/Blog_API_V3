from django.shortcuts import render
from.models import Category,Post,Comment
from.serializers import CategorySerializer,PostSerializer,CommentSerializer
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

class Categoryviewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"

    

    # https://www.cdrf.co/3.1/rest_framework.viewsets/ModelViewSet.html
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
        #     print('data is empty')
        #     return Response({ 'status'  : status.HTTP_400_BAD_REQUEST,
        #                       'message' : 'This field is required'
        #                     })

            raise serializers.ValidationError('This field is required.')

    def perform_create(self, serializer):
       serializer.save()









class Postviewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"



class Commentviewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
