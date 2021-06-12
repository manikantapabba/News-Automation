from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self,email,phone,password=None):
        if not email:
            raise ValueError("Email is required")
        if not phone:
            raise ValueError("phone no is required")

        user=self.model(
            email = self.normalize_email(email),
            phone = phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,phone,password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user




class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=60,unique=True)
    phone = models.CharField(max_length=10)

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['phone']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True
