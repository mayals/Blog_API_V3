from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from.models import Category,Post,Comment,UserModel
from . my_validators import requiredValidator,checkTitleValidator,maxLengthValidator
from rest_framework import status

# https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/#hyperlinking-our-api
# https://www.django-rest-framework.org/api-guide/validators/#uniquevalidator
# https://www.django-rest-framework.org/api-guide/relations/
# https://medium.com/django-rest/django-rest-framework-login-and-register-user-fd91cf6029d5

class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )
    email = serializers.EmailField(
                                    required=True,
                                    validators=[UniqueValidator(queryset=UserModel.objects.all())]
    )
    password  = serializers.CharField(
                                      required=True,
                                      help_text='Leave empty if no change needed',
                                      style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(
                                      required=True,
                                      help_text='Leave empty if no change needed',
                                      style={'input_type': 'password', 'placeholder': 'Password2'}
    )
    url = serializers.HyperlinkedIdentityField(read_only=True,view_name='user-detail',lookup_field='username')
    
    class Meta:
        model  = UserModel 
        fields = [
            'username','email','password','password2',
            'first_name','last_name','gender','born_date','country','avatar','bio','website','url'
        ]
        # write_only_fields = ['password','password2']
        read_only_fields = ['url']
        # extra_kwargs = {'password': {'write_only': True}}


    
    def validate_username(self, value): # work ok :)
        if value is None:
            raise serializers.ValidationError("username field is required",status.HTTP_400_BAD_REQUEST)
        if UserModel.objects.filter(username=value).exists() == True:
            raise serializers.ValidationError(f" '{value}'  this username already been used. Try another username.",status.HTTP_400_BAD_REQUEST) 
        return value
    

    def validate_email(self, value): # work ok :)
        if value is None:
            raise serializers.ValidationError("email field is required",status.HTTP_400_BAD_REQUEST)
        if UserModel.objects.filter(email=value).exists() == True:
            raise serializers.ValidationError(f" '{value}'  this email already been used. Try another email.",status.HTTP_400_BAD_REQUEST)
        return value
    

    def validate(self, data): # work ok :)
        if data['password'] is None:
            raise serializers.ValidationError("password field is required",status.HTTP_400_BAD_REQUEST)
        if data['password2'] is None:
            raise serializers.ValidationError("password2 field is required",status.HTTP_400_BAD_REQUEST)
        if len(data['password']) < 8:
             raise serializers.ValidationError('Password must be  more than 8 Characters.',status.HTTP_400_BAD_REQUEST)
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password and Confirm Password Should be Same!',status.HTTP_400_BAD_REQUEST)  
        return data
       
    # https://www.django-rest-framework.org/api-guide/serializers/#handling-saving-related-instances-in-model-manager-classes
    # https://www.django-rest-framework.org/api-guide/serializers/#additional-keyword-arguments
    # https://github.com/LondonAppDev/course-rest-api/blob/master/src/profiles_project/profiles_api/serializers.py
    def create(self,validated_data):
        
        user = UserModel( 
                    username = validated_data['username'], 
                    email = validated_data['email'],
                    first_name = validated_data['first_name'],
                    last_name = validated_data['last_name'],
                    gender = validated_data['gender'],
                    born_date = validated_data['born_date'],
                    country = validated_data['country'],
                    avatar = validated_data['avatar'],
                    bio = validated_data['bio'],
                    website = validated_data['website'],                                         
        )  
        print(user)
        user.set_password(validated_data['password'])
        user.save()
        return user


    

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name  = validated_data.get('last_name', instance.last_name)
        instance.gender     = validated_data.get('gender', instance.gender)
        instance.born_date  = validated_data.get('born_date', instance.born_date)
        instance.country    = validated_data.get('country', instance.country)
        instance.avatar     = validated_data.get('avatar', instance.avatar)
        instance.website    = validated_data.get('website', instance.website)
        instance.bio        = validated_data.get('bio', instance.bio)
        # password  = validated_data.pop(password)
        # password2 = validated_data.pop(password2)
        instance.save()
        user = UserModel(instance)
        return user






class CategorySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(validators=[
                                            maxLengthValidator,
                                            requiredValidator,# this notwork!
                                            UniqueValidator(queryset=Category.objects.all(),message='يجب أن يكون أسم التصنيف غير مكرر')
                                            ])
    description    = serializers.CharField(required=False) 
    #url - mean -> category detail and use HyperlinkedIdentityField
    url = serializers.HyperlinkedIdentityField(read_only=True,view_name='category-detail',lookup_field='slug')   # view_name='{model_name}-detail'
    posts_category  = serializers.HyperlinkedRelatedField(read_only=True,view_name='post-detail',many=True,lookup_field='slug')
    

    # not work ..no chage has done in message!
    # https://stackoverflow.com/questions/30565389/django-rest-framework-how-to-create-custom-error-messages-for-all-modelseriali
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)

        self.fields['name'].error_messages['required'] = 'This field is required'
        self.fields['name'].error_messages['read_only'] = 'NO EDIT ALOWED'
    
    
    # not work ..no chage has done in message!
    # https://www.django-rest-framework.org/api-guide/serializers/#field-level-validation
    def validate_name(self,value):
        if value is None:
            raise serializers.ValidationError("This field is required",status.HTTP_400_BAD_REQUEST)
        return value


    # work ok all :) to make "name" not allowed for update
    # https://www.appsloveworld.com/django/100/14/how-to-make-a-field-editable-on-create-and-read-only-on-update-in-django-rest-fra
    def update(self, instance, validated_data):
        validated_data.pop('name')                         # validated_data no longer has name     
        super().update(instance, validated_data)
        raise serializers.ValidationError("This field not allowed to update",status.HTTP_400_BAD_REQUEST) 
         


    class Meta:
        model  = Category 
        fields = ['id','name','description','date_add','date_update','url','posts_category'] 
        read_only_fields = ('name','id',)
        extra_kwargs = {
                        "name": {
                             "error_messages": { "required": "Please This field is required" },
                             "max_length": 20  
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
    id            = serializers.UUIDField(read_only=True)
    category      = serializers.SlugRelatedField(
                            queryset = Category.objects.all(),
                            slug_field = 'name'  # to display category_id asredable  use name field  insead of id field 
                            ) 
    title         = serializers.CharField(validators=[
                                                    maxLengthValidator,
                                                    # checkTitleValidator, # work ok
                                                    requiredValidator,#not work!
                                                    UniqueValidator(queryset=Post.objects.all())
                                           ])
    author        = serializers.CharField(required=True)
    body          = serializers.CharField(required=True,style={'base_template': 'textarea.html'} )
    
    
    
    url   = serializers.HyperlinkedIdentityField(read_only=True,view_name='post-detail',lookup_field='slug')  
    comments_post = serializers.HyperlinkedRelatedField(read_only=True,view_name='comment-detail',many=True)
    
    
    class Meta:
        model  = Post 
        fields = ['id','category','title','body','author','date_add','date_update','url','comments_post'] 
        read_only_fields = ('name','id',)











class CommentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.UUIDField(read_only=True)    
    post          = serializers.SlugRelatedField(
                            queryset = Post.objects.all(),
                            slug_field = 'title'  # to display category_id asredable  use name field  insead of id field 
                            ) 
    
    text          = serializers.CharField(required=True,style={'base_template': 'textarea.html'} ) 
    comment_by    = serializers.CharField(required=True)
    allowed       = serializers.BooleanField(default=False)
    

    class Meta:
        model  = Comment 
        fields = ['id','post','text','comment_by','allowed'] 