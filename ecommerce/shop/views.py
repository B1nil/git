from django.shortcuts import render,redirect
from .models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse
from  django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'home.html')

def category(request):
    item=Category.objects.all()

    return render(request,'category.html',{'item':item})

def product(request,i):
    c=Category.objects.get(id=i)
    p=Product.objects.filter(category=c)
    item=Product.objects.all()
    return render(request,'product.html',{'c':c,'p':p})

def details(request,i):
    d=Product.objects.get(id=i)
    return render(request,'details.html',{'d':d})
@login_required()
def register(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']
        cp = request.POST['cp']
        e = request.POST['e']
        fn = request.POST['fn']
        ln = request.POST['ln']
        if (cp == p):
            user = User.objects.create_user(username=u, password=p, email=e, first_name=fn, last_name=ln)
            user.save()
            return redirect('home')

    return render(request,'register.html')

def user_login(request):
    if (request.method == 'POST'):
        u = request.POST['u']
        p = request.POST['p']
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect('shop:home')
        else:
            messages.error(request, 'Invalid Credentials')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('shop:user_login')
