from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'phone', 'address', 'avatar', 'user_type']


class ItemTypeSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField(source="get_item_type_display")

    class Meta:
        model = ItemType
        fields = ['id', 'item_type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['item_type'] = instance.get_item_type_display()
        return representation


class ItemSerializer(serializers.ModelSerializer):
    item_type = serializers.CharField(source="get_item_type_display")
    item_desc = serializers.SerializerMethodField()
    merchant_data = UserSerializer(source='merchant', read_only=True)


    class Meta:
        model = Item
        fields = '__all__'

    def get_item_desc(self, obj):
        try:
            item_desc = ItemDescription.objects.filter(item_id=obj).first()
            item_desc_serializer = ItemDescriptionSerializer(item_desc)
            return item_desc_serializer.data
        except ItemDescription.DoesNotExist:
            pass

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        merchant_data = representation['merchant_data']  # 获取 user 字段的值
        representation.pop('merchant')
        representation['merchant'] = merchant_data['username']  # 添加 制造商名字数据

        desc_data = representation['item_desc']
        representation.pop('item_desc')
        if len(desc_data['desc_imgs']) > 0:
            imgs = desc_data['desc_imgs'].split('[/--sp--/]')
            del (imgs[-1])
            representation['item_desc'] = imgs
        else:
            representation['item_desc'] = ''
        return representation


class ItemDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDescription
        fields = ['itemdesc_id', 'item_id', 'desc_imgs']


class OrderSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'address', 'total', 'order_details', 'phone']

    def get_order_details(self, obj):
        # 查询对应订单的订单详情数据
        order_details = OrderDetail.objects.filter(order_id=obj)
        # 序列化订单详情数据
        order_detail_serializer = OrderDetailSerializer(order_details, many=True)
        return order_detail_serializer.data


class OrderInfoSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'address', 'user_info', 'phone']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = representation['user_info']  # 获取 user 字段的值
        representation.pop('user_info')
        representation['user_info'] = user_data['username']
        return representation


class OrderDetailSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source="get_status_display")
    item = ItemSerializer(source='item_id', read_only=True)
    order = OrderInfoSerializer(source='order_id', read_only=True)

    class Meta:
        model = OrderDetail
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        item_data = representation['item']  # 获取 item 字段的值
        representation.pop('item')
        representation['item_image'] = item_data['item_image']  # 添加 item_image 数据
        representation['item_name'] = item_data['item_name']
        representation['item_type'] = item_data['item_type']
        return representation


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartDetailSerializer(serializers.ModelSerializer):
    item = ItemSerializer(source='item_id', read_only=True)

    class Meta:
        model = CartDetail
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        item_data = representation['item']  # 获取 item 字段的值
        representation.pop('item')
        representation['item_image'] = item_data['item_image']  # 添加 item_image 数据
        representation['item_name'] = item_data['item_name']
        representation['item_type'] = item_data['item_type']
        representation['price'] = item_data['price']
        representation['item_quantity'] = item_data['item_quantity']

        return representation


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
