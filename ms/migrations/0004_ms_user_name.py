# Generated by Django 4.2.3 on 2023-07-25 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ms', '0003_rename_text_ms_user_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='ms_user',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='name_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
