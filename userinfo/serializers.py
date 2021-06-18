from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth import get_user_model
import re

from .models import CustomerProfile, VendorProfile, Comment, UserAddress
User = get_user_model()




class CustomerProfileSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CustomerProfile
        fields = ('id', 'name', 'about', 'email', 'image')

    def validate_email(self, value):
        if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", value):
            raise serializers.ValidationError({'Email':'Please enter a valid email'})
        return value




class VendorProfileSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = VendorProfile
        fields = ('id', 'name', 'about', 'email', 'image')

    def validate_email(self, value):
        if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", value):
            raise serializers.ValidationError({'Email':'Please enter a valid email'})
        return value





def create_comment_serializer(model_type = None,  object_id=None, parent_id=None, user=None):

    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', 'user' ,'content', 'timestamp')
            ref_name = "Comment Create"

        def __init__(self, *args, **kwargs):
        	self.model_type = model_type
        	self.object_id = object_id
        	self.parent_obj = None
        	self.user = user
        	if parent_id:
        		parent_qs = Comment.objects.filter(id = parent_id)
        		if parent_qs.exists() and parent_qs.count() == 1:
        			self.parent_obj = parent_qs.first()

        	return super(CommentCreateSerializer, self).__init__(*args, **kwargs)


        def validate(self, data):
        	model_type = self.model_type
        	model_qs = ContentType.objects.filter(model = model_type)
        	if not model_qs.exists() or model_qs.count() != 1:
        		raise serializers.ValidationError("This is not a valid content type")

        	SomeModel = model_qs.first().model_class()
        	obj_qs = SomeModel.objects.filter(pk = self.object_id)
        	if not obj_qs.exists() or obj_qs.count() != 1:
        		raise serializers.ValidationError("This is not the id for this content type")
        	return data


        def create(self, validated_data):
        	content = validated_data.get('content')
        	if user:
        		main_user = user
        	model_type = self.model_type
        	pk = self.object_id
        	parent_obj = self.parent_obj
        	comment = Comment.objects.create_by_modeltype(
        				model_type, pk, content, main_user,
        				parent_obj = parent_obj)

        	return comment

    return CommentCreateSerializer




class CommentListSerializer(serializers.ModelSerializer):
	reply_count = serializers.SerializerMethodField()
	class Meta:
		model = Comment
		fields = ('id', 'user', 'content', 'reply_count', 'timestamp') #'content_type', 'object_id', 'parent',

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0


class CommentChildSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ('id', 'user', 'content', 'timestamp')



class CommentDetailSerializer(serializers.ModelSerializer):
	replies = serializers.SerializerMethodField()
	reply_count = serializers.SerializerMethodField()
	class Meta:
		model = Comment
		fields = ('id', 'user', 'content', 'replies', 'reply_count', 'timestamp', 'object_id') #'content_type', 'object_id',
		read_only_fields = ('reply_count', 'replies', 'object_id') #'content_type', 'object_id',

	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many = True).data
		return None

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0




class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = "__all__"
        # exclude_field = ('date_added')