from rest_framework import generics

from rest_framework import status, views, viewsets
from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework.decorators import  permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from commons.permissions import IsUserOrReadOnly

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login

from .models import PhoneOTP
from .serializers import (AllUserSerializer, 
                        LoginSerializer, 
                        ChangePasswordSerializer )

from concurrent.futures import ThreadPoolExecutor
from utils.utils import send_otp

User = get_user_model()
executor = ThreadPoolExecutor()


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, format=None):
        serializer = LoginSerializer(data = self.request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(self.request, user)
        return super().post(self.request, format=None)




class UserView(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, IsUserOrReadOnly)
    serializer_class = AllUserSerializer
    permission_classes = [IsAuthenticated,]
    http_method_names = ['get','delete','put','post']

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.filter(phone = self.request.user)

    @action(methods=['post'], detail=True) #url :http://127.0.0.1:8000/users-api/user/3/changephoneotp/
    def changephoneotp(self, *args, **kwargs):
        new_phone = self.request.data.get('new_phone')
        if new_phone:
            user = User.objects.filter(phone = new_phone)

            if user.exists():
                return JsonResponse({
                    'error':'New phone number is already taken'
                    })
    
            thread = executor.submit(send_otp, new_phone)
            otp = thread.result()
            print(otp)
            if otp:
                otp = str(otp)
                old = PhoneOTP.objects.filter(phone__iexact=new_phone)
                if old.exists():
                    old = old.first()
                    if old.count > 7:
                        return JsonResponse({
                            'error':'Maximum otp limits reached. Kindly support our customer care or try with different number'
                            })
                    old.count = old.count + 1
                    old.otp = otp
                    old.save()
                    return Response(otp, status=status.HTTP_200_OK)

                count = 0
                count = count+1
                PhoneOTP.objects.create(
                    phone = new_phone,
                    otp = otp,
                    changephoneOTP = True,
                    count = count
                    )
                return Response('OTP sent successfully.', status=status.HTTP_200_OK)

            return JsonResponse({
                'error':'OTP sending error. Please try after sometime.'
                })

        return JsonResponse({
            'error':'No phone number has been received. Kindly do the POST request.'
            })


    def update(self, request, pk=None):
        otp = self.request.data.get('otp')
        new_phone = self.request.data.get('new_phone')

        if otp and new_phone:
            old = PhoneOTP.objects.filter(Q(phone__iexact = new_phone) & Q(otp__iexact = otp))
            if old.exists():
                old = old.first()

                if str(otp) == str(old.otp):
                    if old.changephoneOTP:
                        user = get_object_or_404(User,id=pk)
                        user.phone = new_phone
                        user.save()
                        old.delete()
                        return Response(new_phone, status=status.HTTP_200_OK)

                    return JsonResponse({
                        'error':'OTP Verification failed. Please verify OTP'
                        }) 

                return JsonResponse({
                    'error':'OTP incorrect, please try again'
                    })

            return JsonResponse({
                'error':'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password'
                })

        return JsonResponse({'error':'Either phone or otp was not recieved in Put request'})



class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)

    def get_object(self):
        return self.request.user

    




