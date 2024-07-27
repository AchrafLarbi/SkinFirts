from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpecializationViewSet, DoctorViewSet, ReviewViewSet, FavoriteDoctorViewSet

router = DefaultRouter()
router.register(r'specializations', SpecializationViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'favorite-doctors', FavoriteDoctorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
