from django.urls import path, include
from rest_framework.routers import DefaultRouter
from store_api import views


router = DefaultRouter()
router.register('tags', views.TagView)
router.register('categories', views.CategoryView)
router.register('products', views.ProductView)
router.register('product-review-history', views.ProductReviewHistory)
router.register('customer-reviews', views.CustomerReviewView)
router.register('users', views.UserView)
router.register('profiles', views.ProfileView)
router.register('orders', views.OrderView)

urlpatterns = [
    path('login/', views.LoginView.as_view()),
    path('', include(router.urls))
]
