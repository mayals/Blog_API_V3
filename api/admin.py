from django.contrib import admin
from.models import Category,Post,Comment
from .models import UserModel



admin.site.register(UserModel)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
