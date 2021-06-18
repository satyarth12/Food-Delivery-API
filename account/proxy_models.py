from .models import User
from django.db import models
from django.contrib.auth import get_user_model

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

User =  get_user_model()


class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "Customer_User", null=True)


	def __str__(self):
		return f'{self.user}'


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        if instance.is_customer == True:
        	Customer.objects.create(user = instance)





class Vendor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "Vendor_User", null=True)

	def __str__(self):
		return f'{self.user}'


@receiver(post_save, sender=User)
def create_vendor(sender, instance, created, **kwargs):
    if created:
    	if instance.is_vendor == True:
        	Vendor.objects.create(user = instance)



# class CustomerManager(models.Manager):

# 	def create_user(self, phone, password, **extra_fields):
# 	    if not phone:
# 	        raise ValueError(_('The Phone must be set'))


# 	    user = self.model(phone=phone, **extra_fields)
# 	    user.set_password(password)
# 	    user.is_customer =True
# 	    user.save(using=self._db)
# 	    return user

# 	def get_queryset(self, *args, **kwargs):
# 		return super().get_queryset(*args, **kwargs).filter(is_customer = True)



# class VendorManager(models.Manager):

# 	def create_user(self, phone, password, **extra_fields):
# 	    if not phone:
# 	        raise ValueError(_('The Phone must be set'))

# 	    user = self.model(phone=phone, **extra_fields)
# 	    user.set_password(password)
# 	    user.is_vendor =True
# 	    user.save(using=self._db)
# 	    return user

# 	def get_queryset(self, *args, **kwargs):
# 		return super().get_queryset(*args, **kwargs).filter(is_vendor = True)




# class Customer(models.Model):
# 	objects = CustomerManager()

# 	class Meta:
# 		proxy = True



# class Vendor(models.Model):
# 	objects = VendorManager()

# 	class Meta:
# 		proxy = True
