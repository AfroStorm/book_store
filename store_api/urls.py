from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store_api import views


router = DefaultRouter()
router.register('tags', views.TagView)

urlpatterns = [
    path('', include(router.urls))
]
