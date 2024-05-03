from django.db import models
from django_starter.db.models import ModelExt
from config.settings import TABLE_PREFIX
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserManager(BaseUserManager):  # 自定义Manager管理器
    def _create_user(self, username, password, phone, user_type=2, **kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        if not phone:
            raise ValueError("请传入电话号码！")
        user = self.model(username=username, phone=phone, user_type=user_type, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, phone, user_type, **kwargs):  # 创建普通用户
        kwargs['is_superuser'] = False
        return self._create_user(username, password, phone, user_type, **kwargs)

    def create_superuser(self, username, password, phone, user_type=0, **kwargs):  # 创建超级用户
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, phone, user_type, **kwargs)


# Create your models here.
class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True, verbose_name='用户ID', help_text='用户ID')
    username = models.CharField(max_length=100, verbose_name='用户名', help_text='用户名', unique=True)
    phone = models.CharField(unique=True, max_length=100, null=True, blank=True, verbose_name='电话', help_text='电话')
    email = models.EmailField(null=True, blank=True, verbose_name='邮箱', help_text='邮箱')
    password = models.CharField(max_length=128, verbose_name='密码', help_text='密码')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='地址', help_text='地址')
    avatar = models.ImageField(upload_to='user/avatar/', null=True, blank=True, verbose_name='头像', help_text='头像')
    user_type_choices = [
        (0, 'Admin'),
        (1, 'Merchant'),
        (2, 'User'),
    ]
    user_type = models.IntegerField(choices=user_type_choices, default=2, verbose_name='用户角色',
                                    help_text='用户角色')

    USERNAME_FIELD = 'username'  # 使用authenticate验证时使用的验证字段，可以换成其他字段，但验证字段必须是唯一的，即设置了unique=True
    REQUIRED_FIELDS = ['phone']  # 创建用户时必须填写的字段，除了该列表里的字段还包括password字段以及USERNAME_FIELD中的字段
    EMAIL_FIELD = 'email'  # 发送邮件时使用的字段

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = TABLE_PREFIX + 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class ItemType(ModelExt):
    item_type_choices = [
        ('Road Frame', '公路车车架'),
        ('Road Wheel', '公路车车轮'),
        ('Road Tire', '公路车轮胎'),
        ('Road Brake', '公路车刹车系统'),
        ('Road Gear System', '公路车变速系统'),
        ('Road Freewheel ', '公路车飞轮'),
        ('Road Pedals', '公路车踏板'),
        ('Road Saddle', '公路车座椅'),
        ('Road Handlebars', '公路车车把'),
        ('Road Fork', '公路车前叉'),
        ('Road Chain', '公路车链条'),
        ('Road Bike', '公路车整车'),

        ('Hill Frame', '山地车车架'),
        ('Hill Wheel', '山地车车轮'),
        ('Hill Tire', '山地车轮胎'),
        ('Hill Brake', '山地车刹车系统'),
        ('Hill Gear System', '山地车变速系统'),
        ('Hill Freewheel ', '山地车飞轮'),
        ('Hill Pedals', '山地车踏板'),
        ('Hill Saddle', '山地车座椅'),
        ('Hill Handlebars', '山地车车把'),
        ('Hill Fork', '山地车前叉'),
        ('Hill Rear Suspension ', '山地车后避震器'),
        ('Hill Chain', '山地车链条'),
        ('Hill Bike', '山地车整车'),

        ('Others', '其他')
    ]
    item_type = models.CharField(max_length=64, choices=item_type_choices, unique=True, verbose_name='商品类型',
                                 help_text='商品类型')

    def __str__(self):
        return self.item_type

    class Meta:
        db_table = TABLE_PREFIX + 'item_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name


class Item(ModelExt):
    item_id = models.BigAutoField(primary_key=True, verbose_name='商品ID', help_text='商品ID')
    item_name = models.CharField(max_length=100, verbose_name='商品名', help_text='商品名')
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE, verbose_name='商品类型', help_text='商品类型')
    item_image = models.ImageField(upload_to='item/image/', null=True, blank=True, verbose_name='商品图片',
                                   help_text='商品图片')
    item_quantity = models.IntegerField(default=0, verbose_name='库存', help_text='库存')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格', help_text='商品价格')
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 1})
    item_status = models.BooleanField(default=True, verbose_name='商品状态', help_text='商品状态')

    def __str__(self):
        return self.item_name

    def get_item_type_display(self):
        return self.item_type.get_item_type_display()

    class Meta:
        db_table = TABLE_PREFIX + 'item'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class ItemDescription(ModelExt):
    itemdesc_id = models.BigAutoField(primary_key=True, verbose_name='商品详情ID', help_text='商品详情ID')
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    desc_imgs = models.CharField(max_length=255, null=True, blank=True, verbose_name='详情图', help_text='详情图')

    def __str__(self):
        return self.itemdesc_id.__str__()

    class Meta:
        db_table = TABLE_PREFIX + 'item_desc'
        verbose_name = '商品详情'
        verbose_name_plural = verbose_name


class Order(ModelExt):
    order_id = models.BigAutoField(primary_key=True, verbose_name='订单号', help_text='订单号')
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 2}, related_name='User')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='下单时间', help_text='下单时间')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='地址', help_text='地址')
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name='电话', help_text='电话')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='总价', help_text='总价')

    def __str__(self):
        return self.order_id.__str__()

    class Meta:
        db_table = TABLE_PREFIX + 'order'
        verbose_name = '订单'
        verbose_name_plural = verbose_name


class OrderDetail(ModelExt):
    orderdetail_id = models.BigAutoField(primary_key=True, verbose_name='订单详情号', help_text='订单详情号')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量', help_text='数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价', help_text='单价')
    merchant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 1}, null=True)
    status_choices = [
        ('tobepaid', '待支付'),
        ('pending', '订单准备中'),
        ('sent', '已发货'),
        ('shipping', '运送中'),
        ('delivered', '已送达'),
        ('confirmed', '已签收'),
        ('commented', '已评价'),
    ]
    status = models.CharField(max_length=64, choices=status_choices, default='tobepaid', verbose_name='订单详情状态',
                              help_text='订单详情状态')
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name='评价', help_text='评价')


    def __str__(self):
        return self.orderdetail_id.__str__()

    class Meta:
        db_table = TABLE_PREFIX + 'order_detail'
        verbose_name = '订单详情'
        verbose_name_plural = verbose_name


class Cart(ModelExt):
    user_id = models.ForeignKey(User, limit_choices_to={'user_type': 2}, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='总价', help_text='总价')

    def __str__(self):
        return self.id.__str__()

    class Meta:
        db_table = TABLE_PREFIX + 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name


class CartDetail(ModelExt):
    cartdetail_id = models.BigAutoField(primary_key=True, verbose_name='购物车详情号', help_text='购物车详情号')
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='数量', help_text='数量', default=0)

    # price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='单价', help_text='单价')

    def __str__(self):
        return self.cartdetail_id.__str__()

    class Meta:
        db_table = TABLE_PREFIX + 'cart_detail'
        verbose_name = '购物车详情'
        verbose_name_plural = verbose_name


class Announcement(ModelExt):
    title = models.CharField(max_length=200, verbose_name='公告', help_text='公告')
    content = models.TextField(verbose_name='公告内容', help_text='公告内容')
    post_date = models.DateTimeField(auto_now_add=True, verbose_name='公告时间', help_text='公告时间')

    def __str__(self):
        return self.title

    class Meta:
        db_table = TABLE_PREFIX + 'announcement'
        verbose_name = '公告'
        verbose_name_plural = verbose_name
