# Generated by Django 5.1.3 on 2024-11-22 13:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_total_cost'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CourierOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_orders', to=settings.AUTH_USER_MODEL, verbose_name='Курьер')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='courier_booking', to='order.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
    ]