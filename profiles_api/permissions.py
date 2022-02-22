from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
   """allow only the user owner to edit his profile"""
   def has_object_permission(self, request, view, obj):
      """check user is trying to edit his/her own profile"""
      # user can visit any profile in the system .. GET is a safe method
      if request.method in permissions.SAFE_METHODS:
         return True
      # if we here, so its PUT or DELETE    
      # so we have to check if the object that the user is trying to update
      # has the same id of the currently logged-in user
      return obj.id == request.user.id

class UpdateOwnStatus(permissions.BasePermission):
   """allow users to update only their own status"""
   def has_object_permission(self, request, view, obj):
      """checks tha tuser is trying his/her own status"""
      # user can visit any status of any user in the system .. GET is a safe method
      if request.method in permissions.SAFE_METHODS:
         return True
      # if we here, so its PUT or DELETE method .. mmm its unsafe ha   
      # so we have to check if the object that the user is trying to update
      # has the same id of the currently logged-in user
      return obj.user_profile.id == request.user.id