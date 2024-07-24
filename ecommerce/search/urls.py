
from django.contrib import admin
from django.urls import path
from .import views
app_name='search'
urlpatterns = [
    path('search/',views.search_product,name='search')
]
