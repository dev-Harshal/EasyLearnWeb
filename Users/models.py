from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from Users.services import create_admin_profile


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        create_admin_profile(user,Profile)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'Admin')
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    profile_photo = models.ImageField(upload_to='ProfilePhotos/', null=True, blank=True,)
    institute = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    role = models.CharField(max_length=10, null=False, blank=False)
    joined_date = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'All Users'

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=13, null=False, blank=False)
    designation = models.CharField(max_length=15, null=False, blank=False)
    department = models.CharField(max_length=25, null=False, blank=False)
    
    def __str__(self):
        return self.id
    
    class Meta:
        db_table = 'Users Profile'