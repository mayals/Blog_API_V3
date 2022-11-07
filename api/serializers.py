from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from.models import Category,Post,Comment

# https://www.django-rest-framework.org/api-guide/validators/#uniquevalidator
# https://www.django-rest-framework.org/api-guide/relations/

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    def required(value):
        if value is None:
            raise serializers.ValidationError('This field is required')
         
    
    name = serializers.CharField(required=True, validators=[
                                                    UniqueValidator(queryset=Category.objects.all())
                                                    ])
    description    = serializers.CharField(required=False) 
    

    #url - maean -> category detail and use HyperlinkedIdentityField
    # url   = serializers.HyperlinkedRelatedField(read_only=True, view_name="category-detail" ,lookup_field = 'slug')
    url = serializers.HyperlinkedIdentityField(read_only=True,view_name='category-detail',lookup_field='slug')
    posts_category  = serializers.HyperlinkedRelatedField(read_only=True,view_name='post-detail',many=True)
    

    class Meta:
        model  = Category 
        fields = ['id','name','slug','description','date_add','date_update','url','posts_category'] 
        
        # extra_kwargs = {
        #             'name' : {'required' : True },
        #             'id'   : {'read_only': True },
        #             'slug' : {'read_only': True },
        #             'posts_category': {
        #                       'read_only'    : True,
        #                       'view_name'    : 'api:post-detail',
        #                       'lookup_field' : 'slug' 
        #                     },
                    
       
        #             'url'  : {
        #                        'read_only'    : True,
        #                        'view_name'    : 'api:category-detail',
        #                        'lookup_field' : 'slug'     
        #                     },                      
        #             }




class PostSerializer(serializers.HyperlinkedModelSerializer):

    def required(value):
        if value is None:
            raise serializers.ValidationError('This field is required')


    category      = serializers.SlugRelatedField(
                            queryset = Category.objects.all(),
                            slug_field = 'name'  # to display category_id asredable  use name field  insead of id field 
                            ) 
    title         = serializers.CharField(required=True, validators=[
                                                    UniqueValidator(queryset=Post.objects.all())
                                           ])
    body          = serializers.CharField(required=True) 
    author        = serializers.CharField(required=True)
    
    # url   = serializers.HyperlinkedIdentityField(read_only=True, view_name="post-detail",lookup_field='slug')
    url   = serializers.HyperlinkedIdentityField(read_only=True,view_name='post-detail',lookup_field='slug')  
    comments_post = serializers.HyperlinkedRelatedField(read_only=True,view_name='comment-detail',many=True)
    
    
    class Meta:
        model  = Post 
        fields = ['id','slug','category','title','body','author','url','comments_post'] 
        






class CommentSerializer(serializers.HyperlinkedModelSerializer):

    def required(value):
        if value is None:
            raise serializers.ValidationError('This field is required')
        
        
    post          = serializers.SlugRelatedField(
                            queryset = Post.objects.all(),
                            slug_field = 'title'  # to display category_id asredable  use name field  insead of id field 
                            ) 
    
    text          = serializers.CharField(required=True) 
    comment_by    = serializers.CharField(required=True)
    allowed       = serializers.BooleanField(default=False)
    

    class Meta:
        model  = Comment 
        fields = ['id','post','text','comment_by','allowed'] 