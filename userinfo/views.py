from rest_framework import permissions, viewsets, generics, status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import api_view, action

from django.db.models import Q
from django.shortcuts import get_object_or_404
from commons.permissions import IsOwnerOrReadOnly

from account.proxy_models import Customer, Vendor

from .models import CustomerProfile, VendorProfile, Comment, UserAddress
from django.contrib.auth import get_user_model
from .serializers import (CustomerProfileSerializer,
                         VendorProfileSerializer,
                         CommentListSerializer, 
                         CommentDetailSerializer, 
                         create_comment_serializer,
                         UserAddressSerializer)

User = get_user_model()



class CustomerProfileView(viewsets.ModelViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    http_method_names = ['get','put']

    def get_queryset(self):
        return CustomerProfile.objects.filter(user = self.request.user)

    def get_object(self):
        return self.request.user.customerprofile



class VendorProfileView(viewsets.ModelViewSet):
    serializer_class = VendorProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    http_method_names = ['get','put']

    def get_queryset(self):
        return VendorProfile.objects.filter(user = self.request.user)

    def get_object(self):
        return self.request.user.vendorprofile

    # @action(methods=['get'], detail = False)
    # def my_recommended_profiles(self, request):
    #     profile = get_object_or_404(CustomerProfile, user = self.request.user)
    #     my_recs = profile.get_recommended_profiles()
    #     return Response(self.serializer_class(my_recs, many=True).data)




class CommentListView(generics.ListAPIView):
    serializer_class = CommentListSerializer

    def get_queryset(self, *args, **kwargs):
        querylist = Comment.objects.select_related('user')
        query = self.request.GET.get('q')
        if query:
            querylist = querylist.filter(
                Q(content__icontains=query)|
                Q(user__icontains=query)) .distinct()
        return querylist




class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated,]

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        object_id = self.request.GET.get('pk')
        parent_id = self.request.GET.get('parent_id', None)
        return create_comment_serializer(
                model_type = model_type,  
                object_id=object_id, 
                parent_id=parent_id, 
                user=self.request.user)



class CommentDetailView(DestroyModelMixin, UpdateModelMixin, generics.RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    lookup_field = 'pk'
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




class UserAddressView(viewsets.ModelViewSet):
    queryset = UserAddress.objects.select_related('user')
    serializer_class = UserAddressSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)


    def create(self, request, *args, **kwargs):
        complete_address = self.request.data.get('complete_address')
        landmark = self.request.data.get('landmark', None)
        city = self.request.data.get('city')
        pincode = self.request.data.get('pincode')
        user = self.request.user.id

        data = {
        'user':user,
        'complete_address': complete_address,
        'landmark':landmark,
        'city':city,
        'pincode':pincode
        }

        serializer = UserAddressSerializer(data = data)
        serializer.is_valid(raise_exception = True)
        address = serializer.save()
        return Response({
            "address": UserAddressSerializer(address).data,
        })