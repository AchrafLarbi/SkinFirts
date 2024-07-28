from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random

class MyUserManager(BaseUserManager):

    def create_user(self, username, email,first_name,last_name, password, **kwags):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a firstname')
        if not last_name:
            raise ValueError('Users must have a lastname')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.is_active  = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email,first_name,last_name, password):
        user = self.create_user(username=username,email=email, password=password,first_name=first_name,last_name=last_name)

        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        return user 

class User(AbstractBaseUser, PermissionsMixin):

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')
    username    = models.CharField(unique=True, max_length=20, validators=[alphanumeric])
    email       = models.EmailField(verbose_name='email address', unique=True, max_length=244)
    first_name  = models.CharField(max_length=30, null=True, blank=True)
    last_name   = models.CharField(max_length=50, null=True, blank=True)
    is_active   = models.BooleanField(default=True, null=False)
    is_staff    = models.BooleanField(default=False, null=False)
    image = models.ImageField(upload_to='images/', default='images/default_profile.JPG', blank=True, null=True)
    # token = models.CharField(max_length=255, default="",blank=True, null=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    
    objects = MyUserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','last_name','first_name']

    def get_full_name(self):
        fullname = self.first_name+" "+self.last_name
        return self.fullname

    def get_short_name(self):
        return self.username

    def str(self):
        return self.email
    
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]  # Use of list comprehension
        code_items_for_otp = []

        for i in range(6):
            num = random.choice(number_list)
            code_items_for_otp.append(num)

        code_string = "".join(str(item) for item in code_items_for_otp)  # list comprehension again
        # A six digit random number from the list will be saved in top field
        self.otp = code_string
        super().save(*args, **kwargs)