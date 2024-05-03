from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import *

router = DefaultRouter()

router.register('user', UserViewSet, basename='user')

router.register('item_type', ItemTypeViewSet, basename='item_type')

router.register('item', ItemViewSet, basename='item')

router.register('item_desc', ItemDescriptionViewSet, basename='item')

router.register('order', OrderViewSet, basename='order')

router.register('order_detail', OrderDetailViewSet, basename='order_detail')

router.register('cart', CartViewSet, basename='cart')

router.register('cart_detail', CartDetailViewSet, basename='cart_detail')

router.register('announcement', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls))
]
