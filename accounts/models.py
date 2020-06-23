from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, company, phone, is_active=True, is_admin=False, is_staff=False, is_dealer=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")
        if not company:
            raise ValueError("Users must have a company")
        if not phone:
            raise ValueError("Users must have a phone number")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.company = company
        user_obj.phone = phone
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.dealer = is_dealer
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, email, first_name, last_name, company, phone, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            company,
            phone,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user

    def create_company_staff_user(self, email, first_name, last_name, company, phone, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            company,
            phone,
            password=password,
            is_staff=True
        )
        return user

    def create_dealer_user(self, email, first_name, last_name, company, phone, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            company,
            phone,
            password=password,
            is_dealer=True
        )
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True) # can login
    online = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    dealer = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = ['first_name', 'last_name', 'company', 'phone']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_dealer(self):
        return self.dealer  

    @property
    def is_active(self):
        return self.active

    @property
    def is_online(self):
        return self.online  