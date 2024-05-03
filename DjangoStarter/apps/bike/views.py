from django.shortcuts import render
from typing import Optional


# Create your views here.
class LoginResult(object):
    def __init__(
            self, is_successful: bool,
            user_type: Optional[int] = None,
            token: Optional[str] = None
    ):
        """

        :param is_successful: 是否成功
        :param user_type: 用户类型
        :param token:
        """
        self.is_successful = is_successful
        self.user_type = user_type
        self.token = token

    def to_dict(self):
        return {
            'user_type': self.user_type,
            'token': self.token
        }


class ProfileResult(object):
    def __init__(
            self, is_successful: bool,
            user_profile: Optional[dict] = None,
    ):
        """
        :param is_successful: 是否成功
        :param user_profile: 用户数据，使用 Serializer 序列化
        """
        self.is_successful = is_successful
        self.user_profile = user_profile

    def to_dict(self):
        return {
            'data': self.user_profile
        }


'''
    商品种类结果
'''


class ItemTypeResult(object):
    def __init__(
            self, is_successful: bool,
            itemType_profile: Optional[dict] = None,
    ):
        """
        :param is_successful: 是否成功
        :param item_profile: 用户数据，使用 Serializer 序列化
        """
        self.is_successful = is_successful
        self.itemType_profile = itemType_profile

    def to_dict(self):
        return {
            'data': self.itemType_profile
        }


'''
    商品结果
'''


class ItemResult(object):
    def __init__(
            self, is_successful: bool,
            item_profile: Optional[dict] = None,
    ):
        """
        :param is_successful: 是否成功
        :param item_profile: 用户数据，使用 Serializer 序列化
        """
        self.is_successful = is_successful
        self.item_profile = item_profile

    def to_dict(self):
        return {
            'data': self.item_profile
        }


'''
    商品结果
'''


class CartDetailResult(object):
    def __init__(
            self, is_successful: bool,
            cart_profile: Optional[dict] = None,
            cart_total: Optional[str] = None
    ):
        """
        :param is_successful: 是否成功
        :param cart_profile: 购物车详情数据，使用 Serializer 序列化
        """
        self.is_successful = is_successful
        self.cart_profile = cart_profile
        self.cart_total = cart_total

    def to_dict(self):
        return {
            'data': self.cart_profile,
            'total': self.cart_total
        }


class OrdersDetailResult(object):
    def __init__(
            self, is_successful: bool,
            orders_profile: Optional[dict] = None,
            # order_status: Optional[str] = None,
            # order_total: Optional[str] = None
    ):
        """
        :param is_successful: 是否成功
        :param order_profile: 订单详情数据，使用 Serializer 序列化
        :param order_status: 订单状态
        :param order_total: 订单总价
        """
        self.is_successful = is_successful
        self.orders_profile = orders_profile
        # self.order_status = order_status
        # self.order_total = order_total

    def to_dict(self):
        return {
            'data': self.orders_profile,
            # 'status': self.order_status,
            # 'total': self.order_total
        }
