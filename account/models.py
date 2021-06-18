from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

from .managers import CustomUserManager
from commons import models as common
from commons.models import BaseClass

from django.utils.translation import ugettext_lazy as _
# from restaurant.models import Item



class User(AbstractBaseUser, PermissionsMixin, common.BaseClass):

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message='Phone number must be entered in the format: "9999999999".')
    phone = models.CharField(max_length=15, validators=[phone_regex], unique=True)



    is_customer = models.BooleanField(default=False, null=True)
    is_vendor = models.BooleanField(default=False, null=True)
   
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    def __str__(self):
        return self.phone





class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)

    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')

    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')

    changephoneOTP    = models.BooleanField(default = False, help_text = 'Only true if the change phone OTP action is called')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)








