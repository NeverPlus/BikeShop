import base64
import os

from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from rest_framework.authtoken.models import Token

from config.settings import MEDIA_ROOT
from .models import *
from .serializers import UserSerializer
from .views import LoginResult, ProfileResult

'''
    用户方法
'''


def get_user_by_token(token):
    token_obj = Token.objects.get(key=token)
    user_id = token_obj.user_id
    db_user = User.objects.get(user_id=user_id)
    return db_user


def login_by_password(request, username, password) -> LoginResult:
    """
    使用用户名、密码登录

    :param request:
    :param username:
    :param password:
    :return: 是否成功, user_data, profile_data, token
    """
    db_user: User = User.objects.filter(username=username).first()
    if db_user is None:
        return LoginResult(False)
    pwd_check = check_password(password, db_user.password)
    if not pwd_check:
        return LoginResult(False)

    # 获取用户类型
    user_type = db_user.user_type

    # 生成token
    token, created = Token.objects.get_or_create(user=db_user)

    return LoginResult(True, user_type, token.key)


def profile_by_token(request, token) -> ProfileResult:
    """
        使用TOKEN获取用户数据

        :param request:
        :param token:
        :return: 是否成功, user_profile
        """
    db_user = get_user_by_token(token)
    if db_user is None:
        return ProfileResult(False)
    user_profile = UserSerializer(db_user).data

    return ProfileResult(True, user_profile)


def update_avatar_by_token(token, avatar):
    db_user = get_user_by_token(token)
    if db_user is None:
        return ProfileResult(False)
    avatar_data = base64.b64decode(avatar)
    avatar_name = '%s.jpg' % db_user.username
    avatar_url = 'user/avatar/' + avatar_name
    image_url = os.path.join(MEDIA_ROOT, avatar_url).replace('\\', '/')
    if os.path.exists(image_url):
        os.remove(image_url)
    db_user.avatar.save(avatar_name, ContentFile(avatar_data))
    db_new_user = get_user_by_token(token)
    user_profile = UserSerializer(db_new_user).data
    return ProfileResult(True, user_profile)


def update_profile_by_token(token, username='', email='', phone='', address=''):
    db_user = get_user_by_token(token)
    if db_user is None:
        return ProfileResult(False)
    if username:
        db_user.username = username
    if email:
        db_user.email = email
    if phone:
        db_user.phone = phone
    if address:
        db_user.address = address
    db_user.save()
    db_new_user = get_user_by_token(token)
    user_profile = UserSerializer(db_new_user).data
    return ProfileResult(True, user_profile)


'''
    购物车方法
'''


def get_cart_by_token(token):
    token_obj = Token.objects.get(key=token)
    user_id = token_obj.user_id
    db_user = User.objects.get(user_id=user_id)

    try:
        db_cart = Cart.objects.get(user_id=db_user.user_id)
    except Cart.DoesNotExist:
        new_cart = Cart.objects.create(user_id=db_user)
        return new_cart
    return db_cart


def get_cart_total(cart: Cart):
    total = 0
    try:
        db_cartDetail = CartDetail.objects.filter(cart_id=cart.id)
    except CartDetail.DoesNotExist:
        return total

    for item in db_cartDetail:
        db_item = Item.objects.get(item_id=item.item_id.item_id)
        subtotal = item.quantity * db_item.price
        total = total + subtotal

    return total


'''
    订单方法
'''


def get_orders_by_token(token):
    token_obj = Token.objects.get(key=token)
    user_id = token_obj.user_id
    db_user = User.objects.get(user_id=user_id)

    try:
        db_orders = Order.objects.filter(user=db_user.user_id)
    except Cart.DoesNotExist:
        return None
    return db_orders


def merchant_orders_by_token(token):
    token_obj = Token.objects.get(key=token)
    merchant_id = token_obj.user_id
    db_merchant = User.objects.get(user_id=merchant_id)

    try:
        db_orders = OrderDetail.objects.filter(merchant_id=db_merchant.user_id)
        print(db_orders)
    except Cart.DoesNotExist:
        return None
    return db_orders
