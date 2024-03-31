from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Text(models.Model):
    text = models.TextField()

class Data(models.Model):
    pub_date = models.DateTimeField("date")
    text = models.ManyToManyField(Text, null=True)
    from_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='sent_data'  # Add a related_name for the 'from_name' foreign key
    )
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='received_data'  # Add a related_name for the 'name' foreign key
    )


class ms_user(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='name_users')
    contact = models.ManyToManyField(User, null=True)
    photo = models.ImageField(upload_to='static/user_image' , blank=True)
    def __str__(self):
        return f"{self.name}'s ms_user"
