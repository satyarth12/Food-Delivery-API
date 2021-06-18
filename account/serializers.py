from rest_framework import serializers, status
from django.contrib.auth import authenticate

from rest_framework.response import Response

from django.core.validators import RegexValidator
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth import get_user_model

from knox.models import AuthToken

from .proxy_models import Customer, Vendor


User = get_user_model()


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','phone','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CreateVendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','phone','password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_vendor(**validated_data)
        return user




class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'is_vendor', 'is_customer']






class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(max_length=50, min_length=8, write_only=True, style={'input_type': 'password'})
    customer = serializers.CharField(required=False, max_length=100, allow_blank=True)
    vendor = serializers.CharField(required=False, max_length=100, allow_blank=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        customer = attrs.get('customer')
        vendor = attrs.get('vendor')

        check_user = User.objects.filter(phone = phone).first()
        user_customer = Customer.objects.filter(user = check_user)
        user_vendor = Vendor.objects.filter(user = check_user)

        # print(user_customer)
        # print(user_vendor)
        # print(check_user)

        if phone and password:

            if bool(customer) == True:
                if user_customer.exists():
                    log_user = authenticate(request = self.context.get('request'), phone=phone, password=password)

                elif user_vendor.exists():
                    user = Customer.objects.create(user = check_user)
                    check_user.is_customer = True
                    check_user.save()
                    log_user = authenticate(request = self.context.get('request'), phone=phone, password=password)
                    attrs['user'] = log_user
                    return attrs

                else:
                    msg = {'detail': 'Phone number is not registered.','status': status.HTTP_404_NOT_FOUND}
                    raise serializers.ValidationError(msg)

            attrs['user'] = log_user
            return attrs

            if bool(vendor) == True:
                if user_vendor.exists():
                    log_user = authenticate(request = self.context.get('request'), phone=phone, password=password)


                elif user_customer.exists():
                    user = Vendor.objects.create(user = check_user)
                    check_user.is_vendor = True
                    check_user.save()
                    log_user = authenticate(request = self.context.get('request'), phone=phone, password=password)
                    attrs['user'] = log_user
                    return attrs

                else:
                    msg = {'detail': 'Phone number is not registered.','status': status.HTTP_404_NOT_FOUND}
                    raise serializers.ValidationError(msg)

            attrs['user'] = log_user
            return attrs

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='Authorization')


        # attrs['user'] = log_user
        # return attrs






class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, trim_whitespace=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')
        error_messages = {'old_password': {'required': 'Please enter old password'},
                          'new_password': {'required': 'Please enter new password'}}


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                ({'Warning': 'Your old password does not match'},
                status.HTTP_400_BAD_REQUEST) )
        return value


    def update(self, instance, validated_data): 
        instance.set_password(validated_data['new_password'])
        inst = instance.save()
        return Response('Password has been changed successfully', status=status.HTTP_200_OK)




class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

