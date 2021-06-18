from rest_framework import permissions, status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
import threading

from django.db.models import Q
from django.shortcuts import get_object_or_404

from knox.models import AuthToken
from django.contrib.auth import get_user_model
from .models import PhoneOTP
from .proxy_models import Customer, Vendor
from .serializers import (CreateUserSerializer,
                        CreateVendorSerializer,
                        ForgotPasswordSerializer, 
                        AllUserSerializer)

from moredata.models import Refer_Earn_Customer, Refer_Earn_Vendor

from utils.utils import send_otp
from concurrent.futures import ThreadPoolExecutor


User = get_user_model()
executor = ThreadPoolExecutor()


class ReffView(APIView):
    def post(self, *args, **kwargs):
        code = str(self.request.data.get('ref_code'))
        customer = self.request.data.get('customer', None)
        vendor = self.request.data.get('vendor', None)
        
        try:
            if bool(customer):
                reff = Refer_Earn_Customer.objects.get(code=code)
            elif bool(vendor):
                reff = Refer_Earn_Vendor.objects.get(code=code)

            self.request.session['ref_profile'] = reff.id
            # print('id', reff.id)
        except:
            pass
        print(self.request.session.get_expiry_date())  
        return Response(code)


'''
Uncomment and use these functions for getting paid for sharing your referral code to another Customer or Vendor.
'''

# def register_customer_func(ref_profile, user):

#     recommended_by_profile = Refer_Earn_Customer.objects.get(id = ref_profile)
#     registered_user = User.objects.get(id = user.id)
#     registered_profile = Refer_Earn_Customer.objects.get(profile = registered_user.customerprofile)
#     registered_profile.recommended_by = recommended_by_profile.customerprofile.user
#     registered_profile.save()

#     recommended_by_profile.my_recommended_users.add(user)
#     total = 50
#     refer_money = recommended_by_profile.total_refer_money
#     if refer_money != 0:
#         recommended_by_profile.total_refer_money = refer_money+total 
#     else:
#         recommended_by_profile.total_refer_money = total
#     return recommended_by_profile.save()



# def register_vendor_func(ref_profile, user):

#     recommended_by_profile = Refer_Earn_Vendor.objects.get(id = ref_profile)
#     registered_user = User.objects.get(id = user.id)
#     registered_profile = Refer_Earn_Vendor.objects.get(profile = registered_user.vendorprofile)
#     registered_profile.recommended_by = recommended_by_profile.vendorprofile.user
#     registered_profile.save()

#     recommended_by_profile.my_recommended_users.add(user)
#     total = 50
#     refer_money = recommended_by_profile.total_refer_money
#     if refer_money != 0:
#         recommended_by_profile.total_refer_money = refer_money+total 
#     else:
#         recommended_by_profile.total_refer_money = total
#     return recommended_by_profile.save()





#######################################################################################################################################################

class SendPhoneOTP(APIView):
    def post(self, *args, **kwargs):
        phone_number = self.request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)

            if user.exists():
                return Response('User already exists. Reset your password if forgotten.', status = status.HTTP_409_CONFLICT)

            thread = executor.submit(send_otp, phone)
            otp = thread.result()
            print(otp)

            
            if otp:
                otp = str(otp)
                old_otp = PhoneOTP.objects.filter(phone__iexact = phone)

                if old_otp.exists():
                    old_otp = old_otp.first()
                    otp_count = old_otp.count

                    if otp_count > 6:
                        return Response(
                            'Maximum otp limits reached. Kindly support our customer care or try with different number',
                            status= status.HTTP_429_TOO_MANY_REQUESTS)

                    old_otp.otp = otp
                    old_otp.count = otp_count+1
                    old_otp.save()
                    return Response(
                        'OTP sent successfully.',
                        status = status.HTTP_201_CREATED
                        )

                PhoneOTP.objects.create(
                    phone = phone,
                    otp = otp)
                return Response(
                    'OTP sent successfully.',
                    status = status.HTTP_201_CREATED
                    )

            return Response(
                'OTP sending error. Please try after sometime.',
                status = status.HTTP_408_REQUEST_TIMEOUT
                )

        return JsonResponse({
            'error':'No phone number has been received. Kindly do the POST request.'
            })



class ValidateOTP(APIView):
    def post(self, *args, **kwargs):
        phone_number = self.request.data.get('phone',False)
        otp_sent = self.request.data.get('otp',False)

        if phone_number and otp_sent:
            phone = str(phone_number)
            old = PhoneOTP.objects.filter(phone__iexact = phone)

            if old.exists():
                old = old.first()
                otp = old.otp

                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()
                    return Response('OTP matched, Kindly proceed to save password', status = status.HTTP_202_ACCEPTED)

                return Response('OTP incorrect, please try again', status = status.HTTP_404_NOT_FOUND)

            return Response('Incorrect Phone number. Kindly request a new otp with this number', status = status.HTTP_404_NOT_FOUND)

        return JsonResponse({'error':'Either phone or otp was not recieved in Post request'})



class Register(APIView):
    def post(self, *args, **kwargs):
        phone = self.request.data.get('phone', False)
        password = self.request.data.get('password', False)
        customer = self.request.data.get('customer', None)
        vendor = self.request.data.get('vendor', None)

        print(bool(customer))
        print(bool(vendor))

        if phone and password:
            phone = str(phone)
            user = User.objects.filter(phone__iexact = phone)

            if user.exists():
                print(Vendor.objects.all())
                print(Customer.objects.all())
                print(User.objects.all().first())
                return Response('User already exists. Reset your password if forgotten.', status = status.HTTP_409_CONFLICT)

            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()

                if old.logged:
                    data = {'phone':phone, 'password':password}
                    ref_profile = self.request.session.get('ref_profile')

                    if bool(vendor) == True:
                        serializer = CreateVendorSerializer(data = data)
                        serializer.is_valid(raise_exception = True)

                        if ref_profile is not None:

                            user = serializer.save()
                            old.delete()
                            #thread for referred vendor profile
                            executor.submit(register_func, ref_profile, user)

                        else:
                            user = serializer.save()
                            old.delete()
            

                    elif bool(customer) == True:
                        serializer = CreateUserSerializer(data = data)
                        serializer.is_valid(raise_exception = True)

                        if ref_profile is not None:

                            user = serializer.save()
                            old.delete()
                            #thread for referred customer profile
                            executor.submit(register_customer_func, ref_profile, user)

                        else:
                            user = serializer.save()
                            old.delete()

                    

                    return Response({
                        "user": AllUserSerializer(user).data,
                        "token": AuthToken.objects.create(user)[1]
                    })

                return JsonResponse({
                    'error':'Your otp was not verified earlier. Please go back and verify otp'
                    })

            return Response(
                'Phone number not recognised. Kindly request a new otp with this number', 
                status = status.HTTP_404_NOT_FOUND
                )

        return JsonResponse({
            'error':'Either phone or password was not recieved in Post request'
            })



#-------------------------------FORGOT PASSWORD------------------------------------

class PasswordForgot(APIView):
    def post(self, *args, **kwargs):
        phone_number = self.request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)

            if user.exists():
                thread = executor.submit(send_otp, phone)
                otp = thread.result()
                print(phone, otp)

                if otp:
                    otp = str(otp)
                    old = PhoneOTP.objects.filter(phone__iexact = phone)

                    if old.exists():
                        old = old.first()
                        if old.count > 6:
                            return Response(
                                'Maximum otp limits reached. Kindly support our customer care or try with different number',
                                status= status.HTTP_429_TOO_MANY_REQUESTS)

                        old.count = old.count+1
                        old.otp = otp
                        old.save()
                        return Response(
                            'OTP has been sent for password reset.',
                            status = status.HTTP_201_CREATED
                            )

                    count = 0
                    count = count+1
                    PhoneOTP.objects.create(
                        phone = phone,
                        otp = otp,
                        count = count,
                        forgot =True
                        )
                    return Response(
                        'OTP has been sent for password reset.',
                        status = status.HTTP_201_CREATED
                        )

                return Response("OTP sending error. Please try after some time.", status = status.HTTP_408_REQUEST_TIMEOUT )

            return Response('Phone number not recognised. Kindly try a new account for this number', status = status.HTTP_404_NOT_FOUND)



class ValidatePassForgotOTP(APIView):
    def post(self, *args, **kwargs):
        phone = self.request.data.get('phone', False)
        otp_sent = self.request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            print(old)

            if old.exists():
                old = old.first()

                if old.forgot == True:
                    otp = old.otp
                    if str(otp) == str(otp_sent):
                        old.forgot_logged = True
                        old.save()
                        return Response('OTP matched, kindly proceed to create new password', status= status.HTTP_202_ACCEPTED)

                    return JsonResponse('OTP incorrect, please try again', status= status.HTTP_404_NOT_FOUND)

                return JsonResponse({
                    'error':'This phone has not received valid otp for forgot password. Request a new otp or contact help centre.'
                    })

            return Response(
                'Phone number not recognised. Kindly request a new otp with this number', 
                status = status.HTTP_404_NOT_FOUND
                )

        return JsonResponse({'error':'Either phone or otp was not recieved in Post request'})


class ForgotChangePassword(APIView):
    def post(self, *args, **kwargs):
        phone = self.request.data.get('phone', False)
        otp = self.request.data.get('otp', False)
        password = self.request.data.get('password', False)

        if phone and otp and password:
            old = PhoneOTP.objects.filter(Q(phone__iexact = phone) & Q(otp__iexact = otp))
            if old.exists():
                old = old.first()

                if old.forgot_logged:
                    post_data = {
                    'phone':phone,
                    'password':password
                    }
                    user_obj = get_object_or_404(User, phone__iexact = phone)
                    serializer = ForgotPasswordSerializer(data = post_data)

                    if serializer.is_valid():
                        if user_obj:
                            user_obj.set_password(serializer.data.get('password'))
                            user_obj.is_active = True
                            user_obj.save()
                            old.delete()
                            return JsonResponse({'success':'Password changed successfully. Please Login'})


                return Response('OTP Verification failed. Please verify OTP', status= status.HTTP_404_NOT_FOUND)

            return Response(
                'Phone and otp are not matching or a new phone has entered. Request a new otp in forgot password',
                status = status.HTTP_404_NOT_FOUND
                )


        return JsonResponse({'error':'Post request have parameters mising.'})
