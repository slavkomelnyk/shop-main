# Generated by Django 4.2.3 on 2023-07-21 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopsite', '0005_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='coment',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
