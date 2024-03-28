from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    
    path('profile/', views.profile, name='profile'),
    path('register/',views.register, name='register'),
    path('login/',views.login_fun, name='login'),
    path('logout/',views.logout_fun, name='logout'),
]
