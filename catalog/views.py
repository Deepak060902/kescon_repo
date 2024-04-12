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


def collections_catagory(request, catagory):
    catagory = catagory.replace("_"," ")
    category = get_object_or_404(Category, name=catagory)
    products = Product.objects.filter(category=category)
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
        return redirect(referer)
    else:
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


def update_cart(request, item_id, new_quantity):
    try:
        order_item = OrderItem.objects.get(id=item_id)
        order_item.quantity = new_quantity
        order_item.save()

        return JsonResponse({'success': True})
    except OrderItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})

class QuestionListView(ListView):
    model = Product
    context_object_name = 'search_products'
    template_name = "product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""

        if not self.request.user.is_anonymous:
            order = Order.objects.get(customer=self.request.user.customer)
        else:
            order = None

        if self.request.user.is_anonymous:
            order = None
        else:
            try:
                order = Order.objects.get(customer=self.request.user.customer)
            except Order.DoesNotExist:
                order = None

        if search_input:
            context['search_products'] = context['search_products'].filter(name__icontains = search_input)
            context["search_input"] = search_input
        context['order'] = order
        return context