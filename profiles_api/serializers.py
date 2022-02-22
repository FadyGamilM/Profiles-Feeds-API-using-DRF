from rest_framework import serializers
from . import models

class UserSerializer(serializers.Serializer):
   """Serializes the User model fields"""
   email = serializers.CharField()
   name = serializers.CharField()
   password = serializers.CharField()



class UserProfileSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.UserProfile
      fields = ['id', 'name', 'email', 'password']
      # but the password must be write only field as we don't 
      # need our users to see their pass in response
      extra_kwargs = {
         'password': {
            'write_only': True
         }
      }

   # now we need to override the create instance method
   # when ModelSerializer use 'create' method, the validated data
   # will be passed as a parameter to it, so we can use it
   def create(self, validated_data):
      """
      create and return a new user
      """
      user = models.UserProfile(
         email = validated_data['email'],
         name = validated_data['name']
      )
      # hash the password
      user.set_password(validated_data['password'])
      # save the instance
      user.save()
      # return the created instance
      return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):
   """ seralizer for profile feed items """
   class Meta:
      model = models.ProfileFeedItem
      fields = ['id', 'user_profile', 'status_text', 'created_at']
      # we need the user_profile field as read_only field
      # so we don't need to put it on the json object at postman
      # when we are going to create a new Profile_Feed_item instance
      extra_kwargs = {
         'user_profile': {
            'read_only': True
         }
      }
