from rest_framework import status, views, viewsets, generics
from rest_framework.response import Response

from commons.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from django.contrib.auth import get_user_model

from .serializers import FeedbackSerializer, Customer_Refer_EarnSerializer, KitchenRequestSerializer
from .models import Feedback, Refer_Earn_Customer, Refer_Earn_Vendor, KitchenRequest
from userinfo.models import CustomerProfile, VendorProfile


class FeebackView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def create(self, request):
        feed = self.request.data.get('feedback')

        data = {'user':self.request.user.id, 'feed':feed}
        serializer = FeedbackSerializer(data=data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response('Thankyou for your valuable feedback', status=status.HTTP_201_CREATED)



class Refer_EarnView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # serializer_class = Refer_EarnSerializer
    
    def get_queryset(self):
        return Refer_Earn_Customer.objects.prefetch_related().filter(profile = self.request.user.profile)

    def get_my_customer_ref_data(self, request):
        profile = CustomerProfile.objects.prefetch_related('user').get(user = self.request.user)
        data = Refer_Earn_Customer.objects.prefetch_related('profile').filter(profile = profile)
        return Response(Customer_Refer_EarnSerializer(data, many=True).data)





class KitchenRequestView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = KitchenRequestSerializer


    def get_queryset(self):
        return KitchenRequest.objects.select_related('user').filter(user = self.request.user)