from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# https://docs.djangoproject.com/en/3.2/ref/models/#models

class Category(models.Model):
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