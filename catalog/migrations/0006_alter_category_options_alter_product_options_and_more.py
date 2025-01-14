# Generated by Django 5.1.3 on 2024-12-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_product_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категории', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукты', 'verbose_name_plural': 'Продукты'},
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=15),
        ),
    ]
