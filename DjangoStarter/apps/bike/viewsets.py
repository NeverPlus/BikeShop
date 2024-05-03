import base64
import os.path
import random
import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from config.settings import MEDIA_ROOT
from django_starter.http.response import responses
from .models import *
from .serializers import *
from .services import *
from .views import *


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有用户资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定用户资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加用户资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定用户资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定用户资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定用户资料'))
class UserViewSet(viewsets.ModelViewSet):
    """用户相关操作"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='登录')
    def login(self, request):
        # self.permission_classes = [permissions.AllowAny]
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')

            result: LoginResult = login_by_password(request, username, password)

            if not result.is_successful:
                return responses.unauthorized('登录失败，用户名或密码错误')

            return responses.ok('登录成功', result.to_dict())

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='注册')
    def register(self, request):
        if request.method == 'POST':
            username = request.data.get('username')
            password = request.data.get('password')
            confirm_password = request.data.get('checkPass')
            phone = request.data.get('phone')
            email = request.data.get('email')
            user_type = request.data.get('character')

        if password != confirm_password:
            return responses.bad_request('密码不一致！')

        if User.objects.filter(username=username).exists():
            return responses.bad_request('用户名/邮箱已存在！')

        user_obj = User.objects.create_user(username, password, phone, int(user_type), email=email)

        result: LoginResult = login_by_password(request, username, password)

        return responses.ok('注册成功！', result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='注销用户', manual_parameters=[
        openapi.Parameter(name='token', in_=openapi.IN_QUERY, description='输入token', type=openapi.TYPE_STRING)
    ])
    def unregister(self, request):
        token = request.GET.get('token')
        try:
            db_token = Token.objects.get(key=token)
        except db_token.DoesNotExist:
            pass
        db_token.delete()
        db_user = get_user_by_token(token)
        db_user.delete()

        return responses.ok('注销成功！')

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取用户信息', manual_parameters=[
        openapi.Parameter(name='token', in_=openapi.IN_QUERY, description='输入token', type=openapi.TYPE_STRING)
    ])
    def profile(self, request):
        if request.method == 'GET':
            token = request.GET.get('token')

            if token is None:
                return responses.bad_request('未登录/未注册/用户数据错误')

            result: ProfileResult = profile_by_token(request, token)

        return responses.ok('获取成功！', result.to_dict())

    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(operation_summary='更新用户头像')
    def update_avatar(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            new_avatar = request.data.get('avatarBase64')
            image_type = request.data.get('imageType')

            result: ProfileResult = update_avatar_by_token(token, new_avatar)

            return responses.ok('更新成功！', result.to_dict())

    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(operation_summary='更新用户信息')
    def update_profile(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            new_username = request.data.get('username')
            new_email = request.data.get('email')
            new_phone = request.data.get('phone')
            new_address = request.data.get('address')

            result: ProfileResult = update_profile_by_token(token, new_username, new_email, new_phone, new_address)

            return responses.ok('更新成功！', result.to_dict())

    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(operation_summary='更新用户密码')
    def update_password(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            old_password = request.data.get('oldPassword')
            new_password = request.data.get('newPassword')
            db_user = get_user_by_token(token)

            password_correct = db_user.check_password(old_password)
            if password_correct:
                db_user.set_password(new_password)
                db_user.save()
                return responses.ok('更新成功！')
            else:
                return responses.bad_request('密码不正确')

    @action(detail=False, methods=['POST'])
    @swagger_auto_schema(operation_summary='更新用户密码')
    def forget_password(self, request):
        if request.method == 'POST':
            username = request.data.get('username')
            phone = request.data.get('phone')
            new_password = request.data.get('newPassword')
            try:
                db_user = User.objects.get(username=username)
            except User.DoesNotExist:
                return responses.bad_request('用户不存在')

            if phone == db_user.phone:
                db_user.set_password(new_password)
                db_user.save()
                return responses.ok('重置密码成功！')
            else:
                return responses.bad_request('电话号码不正确')


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有商品种类资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定商品种类资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加商品种类资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定商品种类资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定商品种类资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定商品种类资料'))
class ItemTypeViewSet(viewsets.ModelViewSet):
    """商品种类相关操作"""
    serializer_class = ItemTypeSerializer
    queryset = ItemType.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取所有商品种类')
    def get_itemType(self, request):
        if request.method == 'GET':
            itemType_profile = ItemTypeSerializer(self.queryset, many=True).data
            itemType_result = ItemTypeResult(True, itemType_profile)
            return responses.ok('获取成功！', itemType_result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取对应自行车商品种类')
    def get_item_type(self, request):
        if request.method == 'GET':
            bike_type = request.GET.get('bikeType')

            db_itemTypes = ItemType.objects.filter(item_type__contains=bike_type).exclude(item_type=bike_type + ' Bike')
            db_others = ItemType.objects.filter(item_type='Others')
            db_itemTypes = db_others | db_itemTypes

            itemType_profile = ItemTypeSerializer(db_itemTypes, many=True).data
            itemType_result = ItemTypeResult(True, itemType_profile)
            return responses.ok('获取成功！', itemType_result.to_dict())


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有商品详情资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定商品详情资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加商品详情资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定商品详情资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定商品详情资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定商品详情资料'))
class ItemDescriptionViewSet(viewsets.ModelViewSet):
    """商品详情相关操作"""
    serializer_class = ItemDescriptionSerializer
    queryset = ItemDescription.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='添加商品详情图')
    def add_desc(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            item_name = request.data.get('name')
            image_list = request.data.get('imgString')

            # 找对应的商品
            try:
                db_item = Item.objects.get(item_name=item_name)
            except Item.DoesNotExist:
                return responses.bad_request('商品不存在')

            # 新建对应的商品详情
            try:
                db_itemDesc = ItemDescription.objects.get(item_id=db_item)
            except ItemDescription.DoesNotExist:
                db_itemDesc = ItemDescription.objects.create(item_id=db_item)

            # 处理图片
            # 数据库图片引用链
            images_url = ''
            # 文件夹后缀
            folder_web_url = 'item/desc/%s/' % db_item.item_name
            # 文件夹本地路径
            folder_url = os.path.join(MEDIA_ROOT, folder_web_url).replace('\\', '/')
            if not os.path.isdir(folder_url):
                os.makedirs(folder_url)
            # 遍历商品图数据
            for index, image in enumerate(image_list):
                # 解码图片和种类
                image_data = base64.b64decode(image['imageBase64'])
                image_type = image['imageType']
                # 图片名
                image_name = db_item.item_id.__str__() + '_%s.%s' % (index.__str__(), image_type)

                # 图片本地路径
                image_url = folder_url + image_name
                if os.path.exists(image_url):
                    os.remove(image_url)
                with open(image_url, 'wb') as out:
                    out.write(image_data)  # 再写入文件
                    out.flush()
                    # 图片后缀路径
                images_url += '/media/' + folder_web_url + image_name + '[/--sp--/]'  # 拼接URL，
            db_itemDesc.desc_imgs = images_url
            db_itemDesc.save()

            return responses.ok('完成')

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='修改商品详情图')
    def edit_desc(self, request):
        if request.method == 'POST':
            item_id = request.data.get('itemId')
            image_list = request.data.get('imgString')

            try:
                db_item = Item.objects.get(item_id=item_id)
            except Item.DoesNotExist:
                return responses.bad_request('商品不存在!')
            try:
                db_itemDesc = ItemDescription.objects.get(item_id=db_item)
            except ItemDescription.DoesNotExist:
                db_itemDesc = ItemDescription.objects.create(item_id=db_item)

            # 处理图片
            # 数据库图片引用链
            images_url = ''
            # 文件夹后缀
            folder_web_url = 'item/desc/%s/' % db_item.item_name
            # 文件夹本地路径
            folder_url = os.path.join(MEDIA_ROOT, folder_web_url).replace('\\', '/')
            if not os.path.isdir(folder_url):
                os.makedirs(folder_url)
            else:
                shutil.rmtree(folder_url)
                os.makedirs(folder_url)
            # 遍历商品图数据
            for index, image in enumerate(image_list):
                # 解码图片和种类
                image_data = base64.b64decode(image['imageBase64'])
                image_type = image['imageType']
                # 图片名
                image_name = db_item.item_id.__str__() + '_%s.%s' % (index.__str__(), image_type)

                # 图片本地路径
                image_url = folder_url + image_name
                if os.path.exists(image_url):
                    os.remove(image_url)
                with open(image_url, 'wb') as out:
                    out.write(image_data)  # 再写入文件
                    out.flush()
                    # 图片后缀路径
                images_url += '/media/' + folder_web_url + image_name + '[/--sp--/]'  # 拼接URL，
            db_itemDesc.desc_imgs = images_url
            db_itemDesc.save()
            return responses.ok('更新成功！')


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有商品资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定商品资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加商品资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定商品资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定商品资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定商品资料'))
class ItemViewSet(viewsets.ModelViewSet):
    """商品相关操作"""
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='添加商品')
    def add_item(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            item_name = request.data.get('name')
            item_type = request.data.get('type')
            item_quantity = request.data.get('quantity')
            item_price = request.data.get('price')
            item_string = request.data.get('imageBase64')
            image_type = request.data.get('imageType')

            try:
                db_item = Item.objects.get(item_name=item_name)
                return responses.bad_request('商品已存在')
            except Item.DoesNotExist:
                pass

            # 处理制造商和种类
            db_itemtype = ItemType.objects.get(id=item_type)
            db_merchant = get_user_by_token(token)

            # 处理图片
            image_data = base64.b64decode(item_string)
            image_name = db_merchant.username + '_%s%s' % (item_name, image_type)
            image_url = 'item/image/' + image_name
            image_url = os.path.join(MEDIA_ROOT, image_url).replace('\\', '/')
            if os.path.exists(image_url):
                os.remove(image_url)
            item_image = SimpleUploadedFile(image_name, image_data)

            item = Item.objects.create(item_name=item_name, item_type=db_itemtype, item_quantity=int(item_quantity),
                                       price=float(item_price), merchant=db_merchant,
                                       item_image=item_image)

        return responses.ok('添加成功！')

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取单个商品信息', manual_parameters=[
        openapi.Parameter(name='itemId', in_=openapi.IN_QUERY, description='输入商品id', type=openapi.TYPE_STRING)
    ])
    def get_item(self, request):
        if request.method == 'GET':
            item_id = request.GET.get('itemId')

            try:
                db_item = Item.objects.get(item_id=item_id)
            except db_item.DoesNotExist:
                return responses.bad_request('商品不存在')

            item_profile = ItemSerializer(db_item).data
            if item_profile is None:
                return ItemResult(False)
            else:
                result = ItemResult(True, item_profile)
                return responses.ok('获取成功！', result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='搜索商品信息', manual_parameters=[
        openapi.Parameter(name='string', in_=openapi.IN_QUERY, description='输入搜索词', type=openapi.TYPE_STRING)
    ])
    def search_item(self, request):
        if request.method == 'GET':
            search_string = request.GET.get('searchString')

            db_item = Item.objects.filter(item_name__icontains=search_string)
            item_profile = ItemSerializer(db_item, many=True).data
            if item_profile is None:
                return ItemResult(False)
            else:
                result = ItemResult(True, item_profile)
                return responses.ok('获取成功！', result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取同种类商品信息', manual_parameters=[
        openapi.Parameter(name='itemtypeId', in_=openapi.IN_QUERY, description='输入种类id', type=openapi.TYPE_STRING)
    ])
    def get_items_by_type(self, request):
        if request.method == 'GET':
            type_id = request.GET.get('typeId')

            try:
                db_items = Item.objects.filter(item_type_id=int(type_id))
            except Item.DoesNotExist:
                return responses.bad_request('商品不存在')

            item_profile = ItemSerializer(db_items, many=True).data
            if item_profile is None:
                return ItemResult(False)
            else:
                result = ItemResult(True, item_profile)
                return responses.ok('获取成功！', result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取同种类商品信息', manual_parameters=[
        openapi.Parameter(name='itemtypeId', in_=openapi.IN_QUERY, description='输入种类id', type=openapi.TYPE_STRING)
    ])
    def get_bikes(self, request):
        if request.method == 'GET':
            bike_type = request.GET.get('bikeType')

            db_items = Item.objects.filter(item_type__item_type__contains=bike_type).filter(
                item_type__item_type__contains='Bike')
            print(db_items)
            # try:
            #     db_items = Item.objects.filter(item_type_id=int(type_id))
            # except Item.DoesNotExist:
            #     return responses.bad_request('商品不存在')
            #
            item_profile = ItemSerializer(db_items, many=True).data
            # if item_profile is None:
            #     return ItemResult(False)
            # else:
            result = ItemResult(True, item_profile)
            return responses.ok('获取成功！', result.to_dict())
            # return responses.ok('获取成功！')

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取商家商品信息', manual_parameters=[
        openapi.Parameter(name='token', in_=openapi.IN_QUERY, description='输入商家token', type=openapi.TYPE_STRING)
    ])
    def get_merchant_item(self, request):
        if request.method == 'GET':
            token = request.GET.get('token')
            db_Merchant = get_user_by_token(token)
            try:
                db_items = Item.objects.filter(merchant=db_Merchant.user_id)
            except db_items.DoesNotExist:
                return responses.bad_request('还没有商品')

            item_profile = ItemSerializer(db_items, many=True).data
            if item_profile is None:
                return ItemResult(False)
            else:
                result = ItemResult(True, item_profile)
                return responses.ok('获取成功！', result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取推荐信息')
    def get_recommend_item(self, request):
        if request.method == 'GET':
            type = request.GET.get('type')

            # 获取商品列表id
            if type == 'Parts':
                item_ids = list(
                    self.queryset.exclude(item_type__item_type__contains='Bike').values_list('item_id', flat=True))

            elif type == 'Bikes':
                item_ids = list(
                    self.queryset.filter(item_type__item_type__contains='Bike').values_list('item_id', flat=True))

            # 如果商品数量少于4个，直接返回所有商品ID
            if len(item_ids) < 4:
                recommend_items = []
                for item_id in item_ids:
                    item = Item.objects.get(item_id=item_id)
                    recommend_items.append(item)

                recommend_items_profile = ItemSerializer(recommend_items, many=True).data
                result = ItemResult(True, recommend_items_profile)
                return responses.ok('获取成功！', result.to_dict())
                return responses.ok('!')

            # 随机选择4个商品ID
            recommend_item_ids = random.sample(item_ids, 4)
            recommend_items = []
            for item_id in recommend_item_ids:
                item = Item.objects.get(item_id=item_id)
                recommend_items.append(item)

            recommend_items_profile = ItemSerializer(recommend_items, many=True).data

            if recommend_items_profile is None:
                return ItemResult(False)
            else:
                result = ItemResult(True, recommend_items_profile)
                return responses.ok('获取成功！', result.to_dict())

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='修改商品')
    def edit_item(self, request):
        if request.method == 'POST':
            item_id = request.data.get('itemId')
            item_name = request.data.get('name')
            item_type = request.data.get('type')
            item_quantity = request.data.get('quantity')
            item_price = request.data.get('price')
            new_image = request.data.get('image')
            print(item_type)

            try:
                db_item = Item.objects.get(item_id=item_id)
                if len(item_name) <= 0 or item_name is None:
                    item_name = db_item.item_name
                if not isinstance(item_type, int) or item_type is None:
                    item_type = db_item.item_type.id
            except Item.DoesNotExist:
                return responses.bad_request('商品不存在')
            #
            # 处理制造商和种类
            db_itemtype = ItemType.objects.get(id=item_type)
            db_merchant = db_item.merchant
            # 处理数量和是否商上架
            if item_quantity > 0:
                new_status = True
            else:
                new_status = False
            # # 处理图片
            if new_image:
                item_string = request.data.get('imageBase64')
                image_type = request.data.get('imageType')
                image_data = base64.b64decode(item_string)
                # 删掉旧图片
                db_oldimage = db_item.item_image.path
                old_image_url = db_oldimage.replace('\\', '/')
                if os.path.exists(old_image_url):
                    os.remove(old_image_url)
                # 生成新图片
                image_name = db_merchant.username + '_%s.%s' % (item_name, image_type)
                # image_url = 'item/image/' + image_name
                # image_url = os.path.join(MEDIA_ROOT, image_url).replace('\\', '/')
                item_image = ContentFile(image_data, name=image_name)
                db_item.item_image.save(image_name, item_image)

            Item.objects.filter(pk=int(item_id)).update(item_name=item_name, item_type=db_itemtype,
                                                        item_quantity=int(item_quantity),
                                                        price=float(item_price),
                                                        item_status=new_status)
        return responses.ok('更新成功！')

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='删除商品')
    def delete_item(self, request):
        if request.method == 'GET':
            item_id = request.GET.get('itemId')

            try:
                db_item = Item.objects.get(item_id=item_id)
            except Item.DoesNotExist:
                return responses.bad_request('商品不存在')
            # 删除图片
            db_image = db_item.item_image.path
            image_url = db_image.replace('\\', '/')
            if os.path.exists(image_url):
                os.remove(image_url)

            # 删除描述图
            # 文件夹后缀
            folder_web_url = 'item/desc/%s/' % db_item.item_name
            # 文件夹本地路径
            folder_url = os.path.join(MEDIA_ROOT, folder_web_url).replace('\\', '/')
            if os.path.isdir(folder_url):
                shutil.rmtree(folder_url)

            db_item.delete()
        return responses.ok('删除成功！')


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有订单资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定订单资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加订单资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定订单资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定订单资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定订单资料'))
class OrderViewSet(viewsets.ModelViewSet):
    """订单相关操作"""
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='添加单个商品订单')
    def order_single_item(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            item_id = request.data.get('itmeId')
            address = request.data.get('address')
            quantity = request.data.get('quantity')
            price = request.data.get('price')

            # 处理数据
            db_user = get_user_by_token(token)
            db_item = Item.objects.get(item_id=item_id)
            total = int(quantity) * float(price)
            status = 'pending'

            # 新建订单
            new_order = Order.objects.create(user=db_user, status=status, total=total, address=address)
            new_orderDetail = OrderDetail.objects.create(order_id=new_order, item_id=db_item, quantity=quantity,
                                                         price=db_item.price)

            return responses.ok('创建订单成功！')

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary=' 获取商品订单物品信息')
    def get_items(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            items_id = request.data.get('orderItems')

            # 处理数据
            total = 0
            db_items = []
            for item in items_id:
                db_cartDetail = CartDetail.objects.get(cartdetail_id=item)
                db_items.append(db_cartDetail)
                subtotal = db_cartDetail.quantity * db_cartDetail.item_id.price
                total = total + subtotal

            items_data = CartDetailSerializer(db_items, many=True).data
            result = CartDetailResult(True, items_data, str(total))
            return responses.ok('获取订单物品成功！', result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary=' 获取用户所有商品订单信息')
    def get_orders(self, request):
        if request.method == 'GET':
            token = request.GET.get('token')
            db_orders = get_orders_by_token(token)

            orders_profile = []
            for order in db_orders:
                order_profile = OrderSerializer(order).data
                orders_profile.append(order_profile)
            result = OrdersDetailResult(True, orders_profile)

            return responses.ok('获取成功！', result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary=' 获取商家所有商品订单信息')
    def get_merchant_orders(self, request):
        if request.method == 'GET':
            token = request.GET.get('token')
            db_orders = merchant_orders_by_token(token)

            orders_profile = OrderDetailSerializer(db_orders, many=True).data
            result = OrdersDetailResult(True, orders_profile)

            return responses.ok('获取成功！', result.to_dict())

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='添加商品订单')
    def order_items(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            order_items = request.data.get('orderItems')
            address = request.data.get('address')
            phone = request.data.get('phone')
            total = request.data.get('total')
            order_type = request.data.get('orderType')

            # 处理数据和创建订单
            status = 'tobepaid'
            db_user = get_user_by_token(token)
            db_cart = get_cart_by_token(token)
            new_order = Order.objects.create(user=db_user, address=address, phone=phone, total=float(total))
            if order_type == 'cart':
                for item in order_items:
                    db_item = Item.objects.get(item_id=item['itemId'])
                    db_cartDetail = CartDetail.objects.get(item_id=db_item.item_id, cart_id=db_cart)
                    new_orderDetail = OrderDetail.objects.create(order_id=new_order, item_id=db_item,
                                                                 quantity=item['quantity'],
                                                                 price=float(item['price']),
                                                                 status=status,
                                                                 merchant=db_item.merchant)
                    # 减少库存
                    new_quantity = db_item.item_quantity - item['quantity']
                    if new_quantity < 1:
                        db_item.item_quantity = 0
                        db_item.item_status = False
                    else:
                        db_item.item_quantity = new_quantity
                    db_item.save()
                    db_cartDetail.delete()
            elif order_type == 'direct':
                for item in order_items:
                    db_item = Item.objects.get(item_id=item['itemId'])
                    new_orderDetail = OrderDetail.objects.create(order_id=new_order, item_id=db_item,
                                                                 quantity=item['quantity'],
                                                                 price=float(item['price']),
                                                                 status=status,
                                                                 merchant=db_item.merchant)
                    # 减少库存
                    new_quantity = db_item.item_quantity - item['quantity']
                    if new_quantity < 1:
                        db_item.item_quantity = 0
                        db_item.item_status = False
                    else:
                        db_item.item_quantity = new_quantity
                    db_item.save()

            return responses.ok('订单提交成功！')

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='更改订单信息')
    def change_order_status(self, request):
        if request.method == 'POST':
            orderItem_id = request.data.get('orderItemId')
            new_status = request.data.get('newStatus')

            db_orderDetail = OrderDetail.objects.get(orderdetail_id=orderItem_id)
            db_orderDetail.status = new_status
            db_orderDetail.save()

            return responses.ok('更新成功')

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='评价订单')
    def comment_order(self, request):
        if request.method == 'POST':
            orderItem_id = request.data.get('orderItemId')
            comment = request.data.get('comment')

            db_orderDetail = OrderDetail.objects.get(orderdetail_id=orderItem_id)
            if db_orderDetail.status == 'confirmed':
                db_orderDetail.comment = comment
                db_orderDetail.status = 'commented'
                db_orderDetail.save()
                return responses.ok('评价成功')
            else:
                return responses.bad_request('评价失败')


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有订单详情资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定订单详情资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加订单详情资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定订单详情资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定订单详情资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定订单详情资料'))
class OrderDetailViewSet(viewsets.ModelViewSet):
    """订单详情相关操作"""
    serializer_class = OrderDetailSerializer
    queryset = OrderDetail.objects.all()
    permission_classes = [permissions.AllowAny]


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有购物车资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定购物车资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加购物车资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定购物车资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定购物车资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定购物车资料'))
class CartViewSet(viewsets.ModelViewSet):
    """购物车相关操作"""
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='添加购物车')
    def add_item(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            item_id = request.data.get('itemId')
            quantity = request.data.get('quantity')
            price = request.data.get('price')

            db_cart = get_cart_by_token(token)
            db_item = Item.objects.get(item_id=item_id)

            try:
                db_cartDetail = CartDetail.objects.get(cart_id=db_cart.id, item_id=item_id)
                db_cartDetail.quantity = db_cartDetail.quantity + int(quantity)
                db_cartDetail.save()
            except CartDetail.DoesNotExist:
                db_cartDetail = CartDetail.objects.create(cart_id=db_cart, item_id=db_item, quantity=int(quantity))

            # 计算新价格
            db_cart.total = get_cart_total(db_cart)
            db_cart.save()

            return responses.ok('添加成功')

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='添加多个物品到购物车')
    def add_items(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            items = request.data.get('items')

            db_cart = get_cart_by_token(token)
            # print(items)
            # for item in items:
            #     print(item)

            for item in items:

                db_item = Item.objects.get(item_id=item['itemId'])
                try:
                    db_cartDetail = CartDetail.objects.get(cart_id=db_cart.id, item_id=db_item.item_id)
                    db_cartDetail.quantity = db_cartDetail.quantity + int(item['quantity'])
                    db_cartDetail.save()
                except CartDetail.DoesNotExist:
                    db_cartDetail = CartDetail.objects.create(cart_id=db_cart, item_id=db_item,
                                                              quantity=int(item['quantity']))

            # 计算新价格
            db_cart.total = get_cart_total(db_cart)
            db_cart.save()

            return responses.ok('添加成功')

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='修改购物车商品')
    def edit_item(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            cartdetail_id = request.data.get('cartdetail_id')
            quantity = request.data.get('quantity')

            db_cart = get_cart_by_token(token)
            db_cartDetail = CartDetail.objects.get(cartdetail_id=cartdetail_id)

            db_cartDetail.quantity = int(quantity)
            db_cartDetail.save()

            new_total = get_cart_total(db_cart)
            db_cart.total = new_total
            db_cart.save()

            result = CartDetailResult(True, None, str(db_cart.total))
            return responses.ok('修改完成！', result.to_dict())

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(operation_summary='删除购物车商品')
    def delete_item(self, request):
        if request.method == 'POST':
            token = request.data.get('token')
            cartdetail_id = request.data.get('cartdetail_id')

            db_cart = get_cart_by_token(token)
            db_cartDetail = CartDetail.objects.get(cartdetail_id=cartdetail_id)

            db_cartDetail.delete()

            new_total = get_cart_total(db_cart)
            db_cart.total = new_total
            db_cart.save()

            result = CartDetailResult(True, None, str(db_cart.total))
            return responses.ok('删除完成！', result.to_dict())

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(operation_summary='获取购物车商品信息', manual_parameters=[
        openapi.Parameter(name='token', in_=openapi.IN_QUERY, description='token', type=openapi.TYPE_STRING)
    ])
    def get_items(self, request):
        if request.method == 'GET':
            token = request.GET.get('token')
            db_cart = get_cart_by_token(token)

            db_cartDeatail = CartDetail.objects.filter(cart_id=db_cart.id)

            cartDetail_profile = CartDetailSerializer(db_cartDeatail, many=True).data

            result = CartDetailResult(True, cartDetail_profile, str(db_cart.total))

            return responses.ok('获取成功！', result.to_dict())


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有购物车详情资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定购物车详情资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加购物车详情资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定购物车详情资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定购物车详情资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定购物车详情资料'))
class CartDetailViewSet(viewsets.ModelViewSet):
    """购物车详情相关操作"""
    serializer_class = CartDetailSerializer
    queryset = CartDetail.objects.all()
    permission_classes = [permissions.AllowAny]


@method_decorator(name='list', decorator=swagger_auto_schema(operation_summary='获取所有公告资料'))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_summary='获取指定公告资料'))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_summary='添加公告资料'))
@method_decorator(name='update', decorator=swagger_auto_schema(operation_summary='修改指定公告资料'))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(operation_summary='部分修改指定公告资料'))
@method_decorator(name='destroy', decorator=swagger_auto_schema(operation_summary='删除指定公告资料'))
class AnnouncementViewSet(viewsets.ModelViewSet):
    """公告相关操作"""
    serializer_class = AnnouncementSerializer
    queryset = Announcement.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
