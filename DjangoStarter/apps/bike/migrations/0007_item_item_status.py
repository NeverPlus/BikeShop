# Generated by Django 4.1.7 on 2024-04-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0006_alter_user_email_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_status',
            field=models.BooleanField(default=True, help_text='商品状态', verbose_name='商品状态'),
        ),
    ]
