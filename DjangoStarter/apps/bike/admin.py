from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_id', 'username', 'phone', 'email', 'password', 'address', 'user_type', ]


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ['pk', 'id', 'is_deleted', 'created_time', 'updated_time', 'item_type', ]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'item_name', 'item_type', 'price', 'merchant', 'item_quantity', 'item_status', ]


@admin.register(ItemDescription)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['itemdesc_id', 'item_id', 'desc_imgs', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pk', 'is_deleted', 'created_time', 'updated_time', 'order_id', 'user', 'order_date', 'total', ]


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['pk', 'is_deleted', 'created_time', 'updated_time', 'orderdetail_id', 'order_id', 'item_id',
                    'quantity', 'price', 'status']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['pk', 'id', 'is_deleted', 'created_time', 'updated_time', 'user_id', 'total', ]


@admin.register(CartDetail)
class CartDetailAdmin(admin.ModelAdmin):
    list_display = ['pk', 'is_deleted', 'created_time', 'updated_time', 'cartdetail_id', 'cart_id', 'item_id',
                    'quantity', ]


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['pk', 'id', 'is_deleted', 'created_time', 'updated_time', 'title', 'content', 'post_date', ]
