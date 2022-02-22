from django.db import models

# Create your models here.
from django.contrib.auth import models as auth_models
from django.forms import ValidationError

#TODO => create UserManager to be able to create users
class UserProfileManager(auth_models.BaseUserManager):
   """
   Helps django to work with our User custom model
   """
   def create_user(self, email:str, name:str, password:str=None):
      #! ------------------------- some validation checking ------------------------- #
      if not email:
         raise ValidationError("User must have an email")      
      #! ------------------------ then create the user object ----------------------- #
      email = self.normalize_email(email)
      user = self.model(email=email, name=name)
      # set_password : Encrypts the given password before storing it
      user.set_password(password)
      #! -------------------------- save the user instance -------------------------- #
      user.save() #use the same db we created with userProfileManager
      #! --------------------- returns the created user instance -------------------- #
      return user

   def create_superuser(self, email:str, name:str, password:str):
      #! ------------------------ create the super-user object ----------------------- #
      user = self.create_user(
         email=email,
         name=name,
         password=password,      
      )
      user.is_superuser = True
      user.is_staff = True
      #! -------------------------- save the user instance -------------------------- #
      user.save()
      #! --------------------- returns the created user instance -------------------- #
      return user



# create user model
class UserProfile(auth_models.AbstractUser, auth_models.PermissionsMixin):
   """ Override the User model of django """
   username = None
   email = models.EmailField(max_length=255, unique=True)
   name = models.CharField(max_length=255)
   is_active = models.BooleanField(default=True)
   is_staff = models.BooleanField(default=False)
   # NOTE: we can add more fields like phone numbers or whatever we need to store about user here .. 
   objects = UserProfileManager()
   #       also we have to specify the USERNAME_FIELD
   USERNAME_FIELD = 'email' # so our user can login with email instead of username
   REQUIRED_FIELDS = ['name'] # the email address is already required from previous line

   #! Some Helper Functions ..
   def get_full_name(self):
      """ 
      used to get the user fill name
      if we have first and last name we can return both here
      """
      return self.name
   
   def get_short_name(self):
      """ used to get the user's short name """
      return self.name
   
   def __str__(self):
      """ to convert the object to a string, its the string representation of the object """
      return self.email


class ProfileFeedItem(models.Model):
   """profile status updates"""
   # when user profile is deleted, we have to delete it's feeds .. logic ha!
   user_profile = models.ForeignKey(
      'UserProfile',
      on_delete=models.CASCADE
   )
   status_text = models.CharField(max_length=255)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.status_text