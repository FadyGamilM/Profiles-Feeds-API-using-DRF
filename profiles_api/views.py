from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from . import models
from . import serializers
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
# this will solve the error when logged-out user is trying to create a feed item
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class UserProfileViewSet(viewsets.ModelViewSet):
   # define the serializer to be used
   serializer_class = serializers.UserProfileSerializer
   # define how the data of this model (that used by the serializer) can be accessed
   queryset = models.UserProfile.objects.all()
   # add authentication classes variable to this user
   authentication_classes = (TokenAuthentication, )
   permission_classes = (permissions.UpdateOwnProfile,)
   # tell our view which filter to use
   filter_backends = (filters.SearchFilter,)
   # which field we wanna allow user to filter by
   search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
   """Checks email and password and returns an auth token"""
   # define which serializer your viewset will use
   serializer_class = AuthTokenSerializer
   def create(self, request):
      """use the ObtainAuthToken APIView to validate and create a token"""
      return ObtainAuthToken().as_view()(request=request._request)

class ProfileFeedItemViewSet(viewsets.ModelViewSet):
   """CRUD operations on Feed Item resource"""
   # since that this resource is private resource, so we need to ensure the authority
   # we will use the same token type we used for login process
   authentication_classes = (TokenAuthentication,)
   # specify the used serializer
   serializer_class = serializers.ProfileFeedItemSerializer
   # specify how to access the data from DB
   queryset = models.ProfileFeedItem.objects.all()
   # specify the used permission classes
   permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated )
   # we need to ensure that the user_profile field of the ProfileFeedItem
   # instance is set to the current logged-in user, not any other user
   # so we will override the create method as we have our own logic
   # I hate django .. 
   def perform_create(self, serializer):
      """set user_profile field to the logged-in user"""
      # the logged-in user can be accessed by self.request.user
      serializer.save(
         user_profile = self.request.user
      )

# # # class UserList(APIView):
# # #    serializer_class = UserSerializer
# # #    def get(self, request):
# # #       """List All Users"""
# # #       return Response({"data": []})
# # #    def post(self, request):
# # #       """create a new user"""
# # #       serializer = UserSerializer(data=request.data)
# # #       if serializer.is_valid():
# # #          # you can get the data from the request
# # #          name =  serializer.data.get('name')
# # #          #serializer.save()
# # #          return Response({"message": f"Created {name}"}, status=status.HTTP_201_CREATED)
# # #       else:
# # #          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # #    def put(self, request, pk=None):
# # #       """Updating specific user resource"""
# # #       return Response("updated")
# # #    def patch(self, request, pk=None):
# # #       """update only specific fields for specific user resource"""
# # #       return Response("patched")
# # #    def delete(self, request, pk=None):
# # #       """delete specific user resource"""
# # #       return Response("deleted")












