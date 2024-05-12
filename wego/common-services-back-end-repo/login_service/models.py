from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('users need to have an email')
        if not username:
            raise ValueError('users need a username')
        
        try:
            # Attempt to get a user with the given email
            BaseUser.objects.get(email=email)
            # If the above line does not raise an exception, it means a user with that email already exists
            raise ValueError('email is already being used')
        except ObjectDoesNotExist:
            # This block executes if no user with the given email exists, which is the desired condition
            pass

        # Same try catch but for username    
        try:
            BaseUser.objects.get(username=username)
            raise ValueError('username is already being used')
        except ObjectDoesNotExist:
            pass

        
        user = BaseUser(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def verify_user(self, username, password):
        # Raises errors if parameteres are not blank
        if not username:
            raise ValueError('users need to have an email')
        if not password:
            raise ValueError('users need a username')
        
        # check to see if the user exists in the database by searching for the given username
        try:
            entry = BaseUser.objects.get(username = username)
            print(entry.username, "exists")
        except BaseUser.DoesNotExist:
            raise ValueError('user does not exist')
        except Exception as e:
            raise ValueError('An error occured:', str(e))
        
        # check to see if the given password is correct by hashing it and comparing it to the hashed password in the database
        if not entry.check_password(password):
            raise ValueError('incorrect password')
        else:
            print("correct password!")
        
            


    
class BaseUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    