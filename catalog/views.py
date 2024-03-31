from django.shortcuts import render, redirect
from .models import *
import json
import datetime
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse
import datetime
from . utils import cookieCart, cartData, guestOrder


def index(request):
    collection_products = Product.objects.all()[:8]
    special_products = Product.objects.all()[:4]
    special_products = Product.objects.all()[0:4]
    top_products = Product.objects.all()[7:10]
    best_selling_products = Product.objects.all()[10:13]
    customer = Customer.objects.all()
    if request.user.is_anonymous:
        order = None
    else:
        try:
            order = Order.objects.get(customer=request.user.customer)
        except Order.DoesNotExist:
            order = None
    context = {
        'collection_products': collection_products,
        'special_products': special_products,
        'top_products': top_products,
        'order': order,
        'best_selling_products': best_selling_products 
        }

    return render(request, 'index.html', context )

# def collections(request):
#     products = Product.objects.all()
#     if not request.user.is_anonymous:
#         order = Order.objects.get(customer=request.user.customer)
#     else:
#         order = None
#     context = {'order': order,"products": products}
#     return render(request, 'collection.html', context )

def collections_catagory(request, catagory):
    catagory = catagory.replace("_"," ")
    category = get_object_or_404(Category, name=catagory)
    products = Product.objects.filter(category=category)
    # products = Product.objects.get(category.name = catagory)
    if request.user.is_anonymous:
        order = None
    else:
        try:
            order = Order.objects.get(customer=request.user.customer)
        except Order.DoesNotExist:
            order = None
    context = {'order': order,"products": products, "catagory": catagory }
    return render(request, 'collection.html',context )
    

def product_detail(request, name, catagory):
    product = Product.objects.get(name=name)
    if request.user.is_anonymous:
        order = None
    else:
        try:
            order = Order.objects.get(customer=request.user.customer)
        except Order.DoesNotExist:
            order = None
    context = {'order': order,'product':product}
    return render(request, 'product-detail.html', context)


def add_to_cart(request, product_id):
    if request.user.is_anonymous:
        return redirect('catalog:index')
    quantity = int(request.POST.get('quantity', 1))
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=request.user.customer)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += quantity
    order_item.save()
    referer = request.META.get('HTTP_REFERER')

    if referer:
        # Redirect back to the referer URL
        return redirect(referer)
    else:
        # If referer is not available, redirect to a default URL
        return redirect('catalog:cart')


def remove_from_cart(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    order_item.delete()
    return redirect('catalog:cart')

def cart(request):
    if request.user.is_anonymous:
        return redirect('catalog:index')
    Data=cartData(request)
    cartItems=Data['cartItems']
    order=Data['order']
    items=Data['items']
    
    context={'items':items, 'order': order,'cartItems':cartItems}
    return render (request,'cart.html',context)


def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    print('action:',action)
    print('Product:',productId)

    customer = request.user.customer
    product= Product.objects.get(id=productId)   
    order, create= Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
     
    if action=='add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity = (orderItem.quantity-1)
    
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return  JsonResponse('item added',safe=False)



class QuestionListView(ListView):
    model = Product

    context_object_name = 'search_products'
    # ordering = ['-date_created']
    template_name = "product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""

        if not self.request.user.is_anonymous:
            order = Order.objects.get(customer=self.request.user.customer)
        else:
            order = None


        if search_input:
            context['search_products'] = context['search_products'].filter(name__icontains = search_input)
            context["search_input"] = search_input
        context['order'] = order
        return context