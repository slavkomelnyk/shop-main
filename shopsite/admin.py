from django.contrib import admin
from .models import Product, Order,like,OrderItem
admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(like)



# class OrderAdmin(admin.ModelAdmin):
    

#     def get_product_names(self, obj):
#         return ", ".join([item.product.product_name for item in obj.orderitem_set.all()])
#     list_display = ["get_product_names", "name", "email", "status"]
#     get_product_names.short_description = "Products"


admin.site.register(Order)