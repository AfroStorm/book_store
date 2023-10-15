from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store_api import views


router = DefaultRouter()
router.register('tags', views.TagView)
router.register('categories', views.CategoryView)
router.register('products', views.ProductView)

urlpatterns = [
    path('', include(router.urls))
]
