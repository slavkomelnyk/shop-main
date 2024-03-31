from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.urls import reverse
pr = None
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=30)
    text = models.TextField()
    big_text = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='static/image',blank=True)
    comments = GenericRelation(Comment)




class Order(models.Model):
    
    product = models.ManyToManyField(Product,through='OrderItem', null=True)
    name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=254)
    status = models.CharField(max_length=30 ,null=True)

class OrderItem(models.Model):
    class Meta:
        db_table = 'OrderItem2'

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.order} - {self.product} - Quantity: {self.quantity}"


class like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    like_range = models.IntegerField(
        null=True,
        validators=[
            MinValueValidator(1, message="dont like."),
            MaxValueValidator(5, message="like."),
        ]
    )
    coment = models.CharField(max_length=32, blank=True, null=True)


