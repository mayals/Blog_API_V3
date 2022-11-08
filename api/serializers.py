from rest_framework import serializers,response
from rest_framework.validators import UniqueValidator
from.models import Category,Post,Comment



# https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/#hyperlinking-our-api
# https://www.django-rest-framework.org/api-guide/validators/#uniquevalidator
# https://www.django-rest-framework.org/api-guide/relations/



def required(value):
        if value is None:
             raise serializers.ValidationError('This field is required')
        return value

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    name = serializers.CharField(validators=[
                                            required,
                                            UniqueValidator(queryset=Category.objects.all(),message='يجب أن يكون أسم التصنيف غير مكرر')
                                            ])
    description    = serializers.CharField(required=False) 
    

    #url - mean -> category detail and use HyperlinkedIdentityField
    url = serializers.HyperlinkedIdentityField(read_only=True,view_name='category-detail',lookup_field='slug')   # view_name='{model_name}-detail'
    posts_category  = serializers.HyperlinkedRelatedField(read_only=True,view_name='post-detail',many=True)
    


    # https://stackoverflow.com/questions/30565389/django-rest-framework-how-to-create-custom-error-messages-for-all-modelseriali
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)

        self.fields['name'].error_messages['required'] = 'This field is required'
        self.fields['name'].error_messages['read_only'] = 'NO EDIT ALOWED'
    
    
    
    # https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
    def validate_name(self,value):
        if value is None:
            raise serializers.ValidationError("This field is required")
        return value



    # https://www.appsloveworld.com/django/100/14/how-to-make-a-field-editable-on-create-and-read-only-on-update-in-django-rest-fra
    def update(self, instance, validated_data):
        validated_data.pop('name')                            # validated_data no longer has name     
        return super().update(instance, validated_data)
         


    class Meta:
        model  = Category 
        fields = ['id','name','description','date_add','date_update','url','posts_category'] 
        read_only_fields = ('name',)
        extra_kwargs = {
                        "name": {
                            "error_messages": {
                                "required": "Please This field is required"
                            }
                        }
                    }

        # extra_kwargs = {
        #             'name' : {'required' : True },
        #             'id'   : {'read_only': True },
        #             'slug' : {'read_only': True },
        #             'posts_category': {
        #                       'read_only'    : True,
        #                       'view_name'    : 'post-detail',
        #                       'lookup_field' : 'slug' 
        #                     },
                    
       
        #             'url'  : {
        #                        'read_only'    : True,
        #                        'view_name'    : 'category-detail',
        #                        'lookup_field' : 'slug'     
        #                     },                      
        #             }




class PostSerializer(serializers.HyperlinkedModelSerializer):

    def required(self,data):
        if data is None:
            raise serializers.ValidationError('This field is required')
        return data

    category      = serializers.SlugRelatedField(
                            queryset = Category.objects.all(),
                            slug_field = 'name'  # to display category_id asredable  use name field  insead of id field 
                            ) 
    title         = serializers.CharField(required=True, validators=[
                                                    UniqueValidator(queryset=Post.objects.all())
                                           ])
    body          = serializers.CharField(required=True) 
    author        = serializers.CharField(required=True)
    
    
    url   = serializers.HyperlinkedIdentityField(read_only=True,view_name='post-detail',lookup_field='slug')  
    comments_post = serializers.HyperlinkedRelatedField(read_only=True,view_name='comment-detail',many=True)
    
    
    class Meta:
        model  = Post 
        fields = ['id','category','title','body','author','url','comments_post'] 
        






class CommentSerializer(serializers.HyperlinkedModelSerializer):

    def required(self,data):
        if data is None:
            raise serializers.ValidationError('This field is required')
        return data
        
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