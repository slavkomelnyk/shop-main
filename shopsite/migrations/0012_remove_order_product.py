# Generated by Django 4.2.3 on 2023-07-22 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopsite', '0011_alter_like_coment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]
