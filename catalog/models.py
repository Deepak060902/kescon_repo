from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from authentication.models import Customer
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    brand = models.CharField(max_length=100, null=True, blank=True)
    images=models.ImageField(null=True, upload_to ='product_images/')
    stock_quantity = models.PositiveIntegerField(default=0)
    # on_sale = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url


class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True)
    # complete=models.BooleanField(default=False)
    transaction_id=models.CharField(max_length=100,null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id )

    @property  
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping 


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total        


class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=0,null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total
    

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.product.price} each)"


class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address









