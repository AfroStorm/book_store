from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store_api import views


router = DefaultRouter()
router.register('tags', views.TagView)
router.register('categories', views.CategoryView)
router.register('products', views.ProductView)
router.register('users', views.UserView)
router.register('profiles', views.ProfileView)
router.register('pending-orders', views.PendingOrderVIew)

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('update-wishlist/profiles/<int:pk>/',
         views.UpdateWishlistView.as_view()),
    path('', include(router.urls))
]
