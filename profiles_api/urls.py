
from django.contrib import admin
from django.urls import path, include
from .views import UserProfileViewSet, LoginViewSet, ProfileFeedItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# register a new url to this router
router.register('profile', UserProfileViewSet) # its a model viewset so we don't have to provide a basename to django
router.register('login', LoginViewSet, basename="login")
router.register('feed', ProfileFeedItemViewSet)


urlpatterns = [
    path('', include(router.urls) )
]
