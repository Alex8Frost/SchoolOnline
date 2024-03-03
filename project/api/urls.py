from rest_framework import routers
from .views import StudentsViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'students', StudentsViewSet, basename='students')

urlpatterns = [
    path('', include(router.urls)),
]
