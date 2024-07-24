
from django.contrib import admin
from django.urls import path
from .import views
app_name='shop'
urlpatterns = [
    path('',views.home,name='home'),
    path('category',views.category,name='category'),
    path('product/<int:i>',views.product,name='product'),
    path('details/<int:i>',views.details,name='details'),
    path('register',views.register,name='register'),
    path('user_login',views.user_login,name='user_login'),
    path('user_logout',views.user_logout,name='user_logout')
]
