
from django.contrib import admin
from django.urls import path
from .import views
app_name='cart'
urlpatterns = [
    path('cart/<int:i>',views.add_to_cart,name='cart'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('add_to_cart/<int:i>',views.add_to_cart,name='add_to_cart'),
    path('cart_decrement/<int:i>',views.cart_decrement,name='cart_decrement'),
    path('remove/<int:i>',views.remove,name='remove'),
    path('place_order/',views.place_order,name='place_order'),
    path('payment_status/<u>',views.payment_status,name='payment_status'),
    path('order_view/',views.order_view,name='order_view')
]
