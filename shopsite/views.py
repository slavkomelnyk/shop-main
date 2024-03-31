from django.db.models import Q
from django.shortcuts import render ,get_object_or_404 ,redirect
from django.http import HttpResponse ,HttpRequest, HttpResponseForbidden
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_protect
from .models import Product, Order, like,OrderItem
from .forms import OrderForm ,CreateProductForm, DeleteForm ,EditProductForm, LikeForm,QuantityForm,ChangeOrderStatusForm
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.contrib.auth.decorators import login_required
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from ms.models import ms_user
from star_ratings.models import Rating
@login_required
def img(request):

    try:
        current_user_ms = ms_user.objects.get(name=request.user)
        img = current_user_ms.photo
    except ms_user.DoesNotExist:
        # If there is no related ms_user object for the current user, set img to None or provide a default value
        img = None
    return img

import random

def index(request):
    latest_product_list = Product.objects.all()
    
    # Select 2 unique random products from the list
    try:
        selected_products = random.sample(list(latest_product_list), k=9)
    except Exception as e:
        try:
            selected_products = random.sample(list(latest_product_list), k=6)
        except Exception as e:
            try:
                selected_products = random.sample(list(latest_product_list), k=3)
            except Exception as e:
                try:
                    selected_products = random.sample(list(latest_product_list), k=1)
                except Exception as e:
                    selected_products = random.sample(list(latest_product_list), k=0)
        
    context = {
        'latest_product_list': selected_products,
        'img': img(request),
    }

    return render(request, 'index.html', context)





@csrf_protect
def basket(request):
    user_orders = Order.objects.filter(status="basket",name=request.user).distinct()
    for order in user_orders:
        total_price = order.product.all().aggregate(Sum('price'))['price__sum']
        order.total_price = total_price

    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            product_id = request.POST.get('product_id')  # Get the product ID from the request
            product = get_object_or_404(Product, pk=product_id)

            # Create a new order with status='basket' for the current user if it doesn't exist
            new_order, created = Order.objects.get_or_create(name=request.user, status='basket')

            # Add the product to the order with the selected quantity
            order_item, created = OrderItem.objects.get_or_create(order=new_order, product=product)
            order_item.quantity = quantity
            order_item.save()

            return redirect('basket')  # Redirect back to the basket page after adding the product

    else:

        # Pass the initial value to the form
        form = QuantityForm()

    return render(request, 'basket.html', {'user_orders': user_orders, 'OrderItem': OrderItem, 'form': form,'img':img(request),})

    



def user(request, name):
    user = User.objects.get(username=name)
    email = user.email
    objects = Product.objects.filter(user__username__contains=name)
    context = {
        'name': name,
        'user': user,
        'objects': objects,
        'img':img(request),
    }
    return render(request, 'user.html', context)


def search(request, search):
    try:
        search_integer = int(search)  # Assuming 'search' is an integer, handle it appropriately
    except ValueError:
        search_integer = None

    # Use separate Q objects for each field search
    q_product_name = Q(product_name__icontains=search)
    q_text = Q(text__icontains=search)
    q_price = Q(price__icontains=search_integer) if search_integer is not None else Q()
    q_big_text = Q(big_text__icontains=search)
    q_username = Q(user__username__icontains=search)

    objects = Product.objects.filter(q_product_name | q_text | q_price | q_big_text | q_username)
    context = {
        'objects': objects,
        'img':img(request),
    }
    return render(request, 'search.html', context)


@csrf_protect
def detail(request, product_id):
    prod = get_object_or_404(Product, pk=product_id)
    likes = like.objects.order_by("-id")[:5]

    # if request.method == 'POST':
    #     form = LikeForm(request.POST)
    #     if form.is_valid():
    #         # Get the form data
    #         product_id = form.cleaned_data['product_id']
    #         name = form.cleaned_data['name']
    #         like_range = form.cleaned_data['like_range']
    #         comment = form.cleaned_data['comment']
            
    #         # Save the data to the database
    #         product = get_object_or_404(Product, pk=product_id)
    #         like = like(product=product, name=name, like_range=like_range, comment=comment)
    #         like.save()

    # else:
    #     form = LikeForm()

    return render(request, "detail.html", {"product": prod,  "likes": likes,'img':img(request),})






# def results(request, question_id):
#     response = "You're looking at the results of product %s."
#     return HttpResponse(response % question_id)


# def vote(request, question_id):
#     return HttpResponse("You're voting on product %s." % question_id)





@csrf_protect
def order(request, product_id):
    prod = get_object_or_404(Product, pk=product_id)

    # Get the current user
    user = request.user

    # Create a new order with status='basket' for the current user if it doesn't exist
    new_order, created = Order.objects.get_or_create(name=user, status='basket')

    # Add the product to the order
    if new_order.product.filter(pk=prod.pk).exists():
        # The product is already in the order, update its quantity or do nothing
        order_item = OrderItem.objects.filter(order=new_order, product=prod).first()
        if order_item:
            # Increment the quantity if needed, or perform any other actions related to the existing item
            order_item.quantity += 1
            order_item.save()
    else:
        # The product is not in the order, create a new OrderItem and add it to the order
        order_item = OrderItem.objects.create(order=new_order, product=prod)

    # if request.method == 'POST':
    #     form = OrderForm(request.POST)
    #     if form.is_valid():
    #         # Perform any additional actions here if needed

    #         # Redirect to a success page or perform other actions
    #         # For example, redirecting to a thank you page after placing an order
    #         return redirect('../../../../../%s' % product_id)

    # else:
    #     form = OrderForm()

    return render(request, "order.html", {"product": prod,'img':img(request),})


@csrf_protect
def order_buy(request):
    # Assuming 'user' is the name of the authenticated user
    user = request.user

    # Get the order for the authenticated user with status='basket'
    user_order = get_object_or_404(Order, name=user, status='basket')

    # Update the status to 'of' (assuming 'of' is a valid status)
    user_order.status = 'не відправлино'
    user_order.save()

    # Print the updated order (optional)
    print(user_order)

    return HttpResponse("<h1 >корзину відправлено</h1>")





@csrf_protect
def dele(request, pr_id):
    # Get the authenticated user
    user = request.user

    # Get the order for the authenticated user with status='basket'
    user_order = Order.objects.get(name=user, status='basket')

    # pr_id = "Product object (%s)" %pr_id
    user_order.product.remove(pr_id)
    user_order.save()
    return HttpResponse("<h1>продукт з корзини видалено</h1>")




@login_required
def user_menu(request):
    search = request.user.username
    try:
        search_integer = int(search)  # Assuming 'search' is an integer, handle it appropriately
    except ValueError:
        search_integer = None

    # Use separate Q objects for each field search
    q_product_name = Q(product_name__icontains=search)
    q_text = Q(text__icontains=search)
    q_price = Q(price__icontains=search_integer) if search_integer is not None else Q()
    q_big_text = Q(big_text__icontains=search)
    q_username = Q(user__username__icontains=search)

    objects = Product.objects.filter(q_username)
    context = {
        'objects': objects,
        'img':img(request),
    }
    return render(request, 'user_menu.html', context)






def create_product(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            text = form.cleaned_data['text']
            big_text = form.cleaned_data['big_text']
            price = form.cleaned_data['price']
            photo = form.cleaned_data['photo']

            # Assuming you have a logged-in user, you can get the user instance from request
            user = request.user

            # Now create the product with the correct user instance
            prod = Product(user=user, product_name=product_name, text=text, big_text=big_text, price=price, photo=photo)
            prod.save()

            return redirect('../../../../user_menu/')
    else:
        form = CreateProductForm()

    return render(request, 'product_form.html', {'form': form,'img':img(request),})



@csrf_protect
def edit_product(request, product_id):
    prod = get_object_or_404(Product, pk=product_id)

    if request.user != prod.user:
        # If the logged-in user is not the owner of the product, return a forbidden response
        return HttpResponseForbidden("You don't have permission to edit this product.")

    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES)
        if form.is_valid():
            prod.product_name = form.cleaned_data['product_name']
            prod.text = form.cleaned_data['text']
            prod.big_text = form.cleaned_data['big_text']
            prod.price = form.cleaned_data['price']

            photo = form.cleaned_data['photo']
            if photo:
                prod.photo = photo

            prod.save()

            # Redirect to the detail page of the edited product
            return redirect('detail', product_id=product_id)

    else:
        # Populate the form with the current product data
        form = EditProductForm(initial={
            'product_name': prod.product_name,
            'text': prod.text,
            'big_text': prod.big_text,
            'price': prod.price,
        })

    return render(request, 'edit_product.html', {'form': form, 'product': prod,'img':img(request),})




@login_required
def user_orders(request):
    # Retrieve orders for the logged-in user
    user_orders = Order.objects.filter(product__user=request.user).distinct()

    if request.method == 'POST':
        form = ChangeOrderStatusForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            order = Order.objects.get(pk=order_id)
            
            if order.status == "не відправлино":
                new_status = "відправлино"
                order.status = new_status
                order.save()

    else:
        form = ChangeOrderStatusForm()


    for order in user_orders:
        total_price = order.product.all().aggregate(Sum('price'))['price__sum']
        order.total_price = total_price

    return render(request, 'user_orders.html', {'user_orders': user_orders,'form': form,'img':img(request),})


def basket_history(request):
    # Retrieve orders for the logged-in user
    user_orders = Order.objects.filter(name=request.user).distinct()
    # print("Number of orders:", user_orders.count())
    # # Loop through each order and its associated products
    # for order in user_orders:
    #     products = order.product.all()
    #     # Now you can access the products associated with each order
    #     for product in products:
    #         print(product.product_name)  




    if request.method == 'POST':
        form = ChangeOrderStatusForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            order = Order.objects.get(pk=order_id)
            if order.status == "відправлино":
                new_status = "отримано"
                order.status = new_status
                order.save()

    else:
        form = ChangeOrderStatusForm()





    for order in user_orders:
        total_price = order.product.all().aggregate(Sum('price'))['price__sum']
        order.total_price = total_price

    return render(request, 'basket_history.html', {'user_orders': user_orders,'form': form,'img':img(request)})

def delete(request, product_id):
    prod = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        prod.delete()
        return redirect('user_menu')  # Redirect to the user menu page after successful deletion

    return render(request, "delete.html", {"product": prod,'img':img(request),})




def m(request):
    context = {
        'img': img(request),
    }

    return render(request, 'm.html', context)


