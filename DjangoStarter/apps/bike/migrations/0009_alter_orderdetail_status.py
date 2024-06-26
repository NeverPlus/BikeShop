# Generated by Django 4.1.7 on 2024-04-19 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0008_orderdetail_comment_alter_item_item_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='status',
            field=models.CharField(choices=[('tobepaid', '待支付'), ('pending', '订单准备中'), ('sent', '已发货'), ('shipping', '运送中'), ('delivered', '已送达'), ('confirmed', '已签收'), ('commented', '已评价')], default='tobepaid', help_text='订单详情状态', max_length=64, verbose_name='订单详情状态'),
        ),
    ]
