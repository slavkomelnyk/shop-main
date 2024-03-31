from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Order

class ChangeOrderStatusForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput())


# from .models import Product
class OrderForm(forms.Form):
    pass


class QuantityForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1})
    )

class CreateProductForm(forms.Form):
    product_name = forms.CharField(label="Назва", max_length=30)
    text = forms.CharField(label="Текст", widget=forms.Textarea)
    big_text = forms.CharField(label="Довгий текст", widget=forms.Textarea)
    price = forms.DecimalField(label="Ціна", max_digits=8, decimal_places=2)
    photo = forms.ImageField(label="Фото",required=False, widget=forms.FileInput)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= -0.00000000000000001:
            raise forms.ValidationError("Ціна повинна бути більше нуля.")
        return price

    # def clean_photo(self):
    #     photo = self.cleaned_data.get('photo')
    #     if not photo:
    #         raise forms.ValidationError("Фото обов'язково.")
    #     return photo

class DeleteForm(forms.Form):
    pass


class EditProductForm(forms.Form):
    product_name = forms.CharField(label="назва", max_length=30)
    text = forms.CharField(widget=forms.Textarea)
    big_text = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=8, decimal_places=2)
    photo = forms.ImageField(required=False)





class LikeForm(forms.Form):
    product_id = forms.IntegerField()  # Assuming you want to enter the product ID

    # Name field with max length of 30 characters
    name = forms.CharField(max_length=30)

    # Like range field as an IntegerField with validators
    like_range = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="dont like"),
            MaxValueValidator(5, message="like"),
        ]
    )

    # Comment field with max length of 30 characters (optional)
    comment = forms.CharField(max_length=30, required=False)


