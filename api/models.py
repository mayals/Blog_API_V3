from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import uuid
from django.core.mail import send_mail
from .UserModelManger import UserModelManger 
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.core.validators import MinLengthValidator
# https://docs.djangoproject.com/en/3.2/ref/models/#models

#  https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
#  https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#a-full-example
#  https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
#  https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model


 # https://www.youtube.com/watch?v=pIsJ2RPhoFc
class UserModel(AbstractBaseUser,PermissionsMixin):
    
    M = 'Male'
    F = 'Female'
    GENDER_CHOICES=[
                    (M,'Male'),
                    (F,'Female'),
    ]       
    # default user fields:
    username        = models.CharField(max_length=50, null=True, unique=True, editable = False)
    email           = models.EmailField(null = True, unique=True, editable = False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superuser    = models.BooleanField(default=False)
    date_joined     = models.DateTimeField(null=True, auto_now_add=True)
    # Password      this field --> come as default from AbstractBaseUser
    password        = models.CharField( max_length=16,
                                        validators=[MinLengthValidator(8)],
                                        editable = False,
                                        null=True
                                        
    )
    password2       = models.CharField( max_length=16,
                                        validators=[MinLengthValidator(8)],
                                        editable = False,
                                        null=True
    )
    # Last login    this field --> come as default from AbstractBaseUser
    # -------
    # add more fields:
    # we can now add any extra_fields to this UserModel because we customize user model using inherit from AbstractBaseUser 
    first_name      = models.CharField(max_length = 10, null = True)
    last_name       = models.CharField(max_length = 10 ,null = True)
    gender          = models.CharField(choices=GENDER_CHOICES, default='F', max_length=6)
    born_date       = models.DateTimeField(null = True)  
    country         = models.CharField(max_length=30, blank=True, null = True)
    avatar          = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio             = models.TextField(max_length=500, null=True, blank=True)
    website         = models.URLField(max_length=200, null=True, blank=True)
    
    objects = UserModelManger()
    
    USERNAME_FIELD  = 'username' 
    REQUIRED_FIELDS = ['email']
    
    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        # https://www.w3schools.com/python/ref_string_strip.asp
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        # Sends an email to this User.
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    def __str__(self):
        return "{}".format(self.username) 
    
    class Meta:
            ordering = ('first_name',)
            verbose_name = 'UserModel'
            verbose_name_plural = 'UsersModel'






class Category(models.Model):
    id          = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    name        = models.CharField(max_length=20,unique=True,null=True,blank=False)
    slug        = models.SlugField(max_length=25, blank=True, null=True)
    description = models.TextField(null =True,blank=True)
    date_add    = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True,  auto_now_add=False)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('api:category-detail', kwargs = {"slug":self.slug})      #vue view_name='{model_name}-detail'

    def save(self, *args, **kwargs):  
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Call the "real" save() method. 

    
    class Meta:
        ordering =['name']
        verbose_name_plural = "Categories"

   





class Post(models.Model):
    id          = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    category    = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=False,related_name="posts_category")
    title       = models.CharField(max_length=20,null=True,blank=False)
    slug        = models.SlugField(max_length=25, blank=True, null=True)
    author      = models.CharField(max_length=100,null=True,blank=False)
    body        = models.TextField(null=True,blank=False)
    date_add    = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True,  auto_now_add=False)
   
    def __str__(self):
        return self.title 
    class Meta:
        ordering = ['-date_add', 'author']
        unique_together = ['title', 'author']
        
    def get_absolute_url(self):
        return reverse('api:post-detail', kwargs = {"slug":self.slug})      #vue view_name='{model_name}-detail'    
    
    def save(self, *args, **kwargs):  
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Call the "real" save() method.






class Comment(models.Model):
    id          = models.UUIDField(primary_key=True, editable=False,default=uuid.uuid4)
    post        = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=False,related_name="comments_post")
    text        = models.TextField(null=True,blank=False)
    comment_by  = models.CharField(max_length=100,null=True,blank=False)
    allowed     = models.BooleanField(default=False)
    date_add    = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True,  auto_now_add=False)
    
    def __str__(self):
        return f'"{self.text}" by author:{self.comment_by}'

    class Meta:
        ordering = ['-date_add']