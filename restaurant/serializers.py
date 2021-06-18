from rest_framework import serializers
from .models import Item, KitchenAdress, Kitchen, KitchenCuisine, Category
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

# from userinfo.serializers import CommentListSerializer
from userinfo.models import Comment


class CategorySerializer(serializers.ModelSerializer):
    category_name = TagListSerializerField()
    class Meta:
        model = Category
        fields = ['id', 'kitchen', 'category_name', 'about']

    # def get_items_in_category(self, obj):
    #     qs = Item.objects.filter(category = obj)
    #     items = ItemSerializer(qs, many=True).data
    #     return items

    def validate_category_name(self, value):
        if len(value) > 5:
            raise serializers.ValidationError('Enter 1 category at a time.')
        return value

    def create(self, validated_data):
        tags = validated_data.pop('category_name')
        instance = super(CategorySerializer, self).create(validated_data)
        instance.category_name.set(*tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('category_name')
        instance.category_name.set(*tags)
        return instance


class ItemSerializer(TaggitSerializer, serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ['id','kitchen', 'category', 'total_likes', 'name','cost','desc','ingredients','image','image_2','delivery_time','is_available']

    def get_total_likes(self, obj):
        t_qs = obj.likes.count()
        return t_qs



class KitchenCuisineSerializer(TaggitSerializer, serializers.ModelSerializer):
    cuisine_names = TagListSerializerField()
    class Meta:
        model = KitchenCuisine
        fields = ['id', 'kitchen' ,'cuisine_names','kitchen_ranking']

    def validate_cuisine_names(self, value):
        if len(value) > 5:
            raise serializers.ValidationError('Tags more than 5 not allowed.')
        return value


    def create(self, validated_data):
        tags = validated_data.pop('cuisine_names')
        instance = super(KitchenCuisineSerializer, self).create(validated_data)
        instance.cuisine_names.set(*tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('cuisine_names')
        instance.cuisine_names.set(*tags)
        return instance



class KitchenSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    cuisines_present = serializers.SerializerMethodField()
    class Meta:
        model = Kitchen
        fields = ['id','kitchen_name','about','opening_time','closing_time',
                'delivery','takeaway','veg','nonveg','menu_image',
                'kitchen_image','kitchen_welcome_text', 'kitchen_status', 'cuisines_present',
                'user', 'likes', 'total_likes', 'total_comments']

    def get_total_likes(self, obj):
        t_qs = obj.likes.count()
        return t_qs

    def get_total_comments(self,obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        return c_qs.count() 


    def get_cuisines_present(self, obj):
        cuisines = KitchenCuisine.objects.select_related('kitchen').filter(kitchen=obj)
        if cuisines:
            return KitchenCuisineSerializer(cuisines, many=True).data
        return None



class KitchenAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenAdress
        exclude  = ['latitude','longitude']







