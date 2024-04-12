from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 

app_name = "catalog"

urlpatterns = [
    path('', views.index, name='index'),

    path('collections/<str:catagory>', views.collections_catagory, name="collections_catagory"),
    path('collections/<str:catagory>/<str:name>', views.product_detail, name='product_detail'),

    path('cart/', views.cart, name='cart'),
    path('products/', views.QuestionListView.as_view(), name="product-list"),
    
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/<int:new_quantity>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:order_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)