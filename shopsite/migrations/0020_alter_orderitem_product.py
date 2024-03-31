# Generated by Django 4.2.4 on 2023-09-10 11:55

from django.db import migrations, models
import shopsite.models


class Migration(migrations.Migration):

    dependencies = [
        ('shopsite', '0019_alter_orderitem_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=models.SET(shopsite.models.Product), to='shopsite.product'),
        ),
    ]
