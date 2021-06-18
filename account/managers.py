from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError(_('The Phone must be set'))


        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.is_customer = True
        user.save(using=self._db)
        return user

    def create_vendor(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError(_('The Phone must be set'))


        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.is_vendor = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone, password, **extra_fields)