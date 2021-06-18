from django.shortcuts import render, HttpResponse

from rest_framework.views import APIView
from rest_framework import permissions, status, views, viewsets, generics
from commons.permissions import IsOwnerOrReadOnly, IsKitchenOwnerOrReadOnly

from geopy.geocoders import Nominatim
from geopy.distance import  great_circle
from taggit.models import Tag

from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.http import JsonResponse
from django.http import Http404

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from commons.custom_mixins import MultipleFieldLookupMixin

from .serializers import ItemSerializer, KitchenSerializer, KitchenAdressSerializer, KitchenCuisineSerializer, CategorySerializer
from .models import Kitchen, KitchenAdress, Item, KitchenCuisine, Category
from .utils import check_address_distance, takeaway_delivery_filter
from userinfo.serializers import CommentListSerializer
from userinfo.models import Comment, UserAddress

from account.proxy_models import Customer, Vendor


User = get_user_model()


class KitchenView(viewsets.ModelViewSet):
    queryset = Kitchen.objects.select_related().all()
    serializer_class = KitchenSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly,]

    def get_queryset(self, *args, **kwargs):
        return Kitchen.objects.select_related('user')

    def list(self, request):
        user_address = UserAddress.objects.select_related('user').filter(user=self.request.user, active=True).first()
        kitchen_address = KitchenAdress.objects.all().select_related('kitchen')

        if user_address:
            payload = check_address_distance(user_address.pincode, kitchen_address)
            qs = Kitchen.objects.filter(pk__in = payload)
            if qs:
                kitchen = self.serializer_class(qs, many=True).data
                return Response(kitchen)

        qs = Kitchen.objects.all()
        kitchen = self.serializer_class(qs, many=True).data
        return Response(kitchen)


    @action(methods=['get'], detail=True)
    def items_in_kitchen(self, request, pk=None):
        obj = get_object_or_404(Kitchen, id=pk)
        items = Item.objects.select_related('kitchen').filter(kitchen = obj)
        return Response(ItemSerializer(items, many=True).data)

    @action(methods=['get'], detail=True)
    def category_in_kitchen(self, request, pk=None):
        obj = get_object_or_404(Kitchen, id=pk)
        cate = Category.objects.select_related('kitchen').filter(kitchen = obj)
        return Response(CategorySerializer(cate, many=True).data)


    @action(methods=['get'], detail=False)
    def takeaway_kitchen(self, request):
        result = takeaway_delivery_filter(self.serializer_class, self.request.user, 'takeaway')
        return Response(result)


    @action(methods=['get'], detail=False)
    def delivery_kitchen(self, request):
        result = takeaway_delivery_filter(self.serializer_class, self.request.user, 'delivery')
        return Response(result)

    @action(methods=['get'], detail=False)
    def takeaway_delivery_kitchen(self, request):
        result = takeaway_delivery_filter(self.serializer_class, self.request.user, 'both')
        return Response(result)


    action(methods=['put'], detail=True) #url :http://127.0.0.1:8000/home-kitchen/kitchen/3/likeToggle
    def likeToggle(self, request, pk=None):
        user = self.request.user
        kitchen = get_object_or_404(Kitchen, id=pk)
        if user in kitchen.likes.all():
            kitchen.likes.remove(user)
            return Response("Like Removed", status=status.HTTP_200_OK)
        kitchen.likes.add(user)
        return Response("Like Added", status=status.HTTP_200_OK)


    @action(methods=['get'], detail=True) #url :http://127.0.0.1:8000/home-kitchen/kitchen/1/comments
    def comments(self, request, pk=None):
        obj = get_object_or_404(Kitchen, id=pk)
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentListSerializer(c_qs, many=True).data
        return Response(comments)




###########################################################  KITCHEN ADDRESS  ####################################################################

class KitchenAdressView(viewsets.ModelViewSet):
    queryset = KitchenAdress.objects.select_related('kitchen').all()
    serializer_class = KitchenAdressSerializer
    permission_classes = [permissions.IsAuthenticated, IsKitchenOwnerOrReadOnly,]




###########################################################  ITEM  ####################################################################

class ItemView(viewsets.ModelViewSet):
    queryset = Item.objects.select_related().all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsKitchenOwnerOrReadOnly]


    @action(methods=['put'], detail=True) #url :http://127.0.0.1:8000/home-kitchen/item/3/likeToggle
    def likeToggle(self, request, pk=None):
        user = self.request.user
        item = get_object_or_404(Item, id=pk)
        if user in item.likes.all():
            item.likes.remove(user)
            return Response("Like Removed", status=status.HTTP_200_OK)
        item.likes.add(user)
        return Response("Like Added", status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True) #url :http://127.0.0.1:8000/home-kitchen/item/1/comments
    def comments(self, request, pk=None):
        obj = get_object_or_404(Item, id=pk)
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentListSerializer(c_qs, many=True).data
        return Response(comments)





###########################################################  KITCHEN CUISINE  ####################################################################



class KitchenCuisineView(viewsets.ModelViewSet):
    serializer_class = KitchenCuisineSerializer
    permission_classes = [permissions.IsAuthenticated, IsKitchenOwnerOrReadOnly]
    
    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if query:
            return KitchenCuisine.objects.select_related().filter(cuisine_names__slug=query)
        return KitchenCuisine.objects.select_related().all()




class KitchenInCuisineTags(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'slug'

    def retrieve(self, request ,slug=None):
        tag = get_object_or_404(Tag, slug=slug)
        kitchen_cui = KitchenCuisine.objects.select_related().filter(cuisine_names=tag)
        kitch = []
        for KI in kitchen_cui:
            kitch.append(KI.kitchen)
        return Response (KitchenSerializer(kitch, many=True).data)




###########################################################  CATEGORY  ####################################################################


class CategoryTags(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsKitchenOwnerOrReadOnly]
    serializer_class = CategorySerializer

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if query:
            return Category.objects.select_related().filter(category_name__slug=query).all()
        return Category.objects.select_related().all()


    @action(methods=['get'], detail=True)
    def items_in_category(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        items = Item.objects.select_related('kitchen').filter(category=category, kitchen=category.kitchen)
        seri = ItemSerializer(items, many=True).data
        return Response(seri)







