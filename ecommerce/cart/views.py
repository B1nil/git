from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Product
from .models import Cart,Order_table,Payment
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import razorpay


@login_required
def add_to_cart(request,i):
    p=Product.objects.get(id=i)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity +=1
            cart.save()
            p.stock -=1
            p.save()
    except:
        if(p.stock):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -=1
            p.save()

    return redirect('cart:cart_view')

def cart_view(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+i.quantity*i.product.price
    return  render(request,'cart.html',{'c':cart,'total':total})

# def cart_decrement(request,i):
#     p=Product.objects.get(id=i)
#     u=request.user
#     try:
#         cart=Cart.objects.get(user=u,product=p)
#         if(Cart.quantity>1):
#             cart.quantity -=1
#             cart.save()
#             p.stock+=1
#             p.save()
#         else:
#             cart.delete()
#             p.stock +=1
#             p.save()
#     except:
#         pass
#     return redirect('cart:cart_view')
#

# def remove(request,i):
#     p=Product.objects.get(id=i)
#     u=request.user
#     try:
#         cart=Cart.objects.get(user=u,product=p)
#         cart.delete()
#         p.save()
#     except:
#         pass
#     return redirect('cart:cart_view')


def cart_decrement(request, i):
    p = get_object_or_404(Product, id=i)
    u = request.user

    try:
        cart = Cart.objects.get(user=u, product=p)
        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
            messages.success(request, "Product quantity decreased by 1.")
        else:
            cart.delete()
            p.stock += 1
            p.save()
            messages.success(request, "Product removed from cart.")
    except Cart.DoesNotExist:
        messages.error(request, "Product not found in your cart.")

    return redirect('cart:cart_view')


def remove(request, i):
    p = get_object_or_404(Product, id=i)
    u = request.user

    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        messages.success(request, "Product removed from cart successfully.")
    except Cart.DoesNotExist:
        messages.error(request, "Product not found in your cart.")

    return redirect('cart:cart_view')


def place_order(request):
    if(request.method=='POST'):
        ph = request.POST.get('p')
        a = request.POST.get('a')
        n = request.POST.get('n')
        u = request.user
        c = Cart.objects.filter(user=u)  #cart objects
        total=0
        for i in c:
            total=total+(i.quantity*i.product.price)
        total=int(total*100)#total amt

            #create razorpay  client using our API credentials

        client = razorpay.Client(auth=('rzp_test_KjG8ydENFtiZ4P','YFjiW3CMX7Z1Pq164lgbzKrm'))

        #create order in razorpay
        response_payment=client.order.create(dict(amount=total,currency='INR'))
        print(response_payment)
        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status == 'created':
            p = Payment.objects.create(name=u.username, amount=total, order_id=order_id)
            p.save()
            for i in c:
                o=Order_table.objects.create(user=u,product=i.product,address=a,phone=ph,pin=n,no_of_items=i.quantity,order_id=order_id)
                o.save()


        response_payment['name']=u.username
        return render(request,'payment.html',{'payment':response_payment})
    return render(request,'place_order.html')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def payment_status(request,u):
    print(request.user.is_authenticated) #false
    if not request.user.is_authenticated:
        user=User.objects.get(username=u)
        login(request,user)
        print(request.user.is_authenticated)
    if(request.method=='POST'):
        response=request.POST
        # print(response)
        # print(u)
        # to validate the payment request
        param_dict={
            'razorpay_order_id':response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature']
        }
        client = razorpay.Client(auth=('rzp_test_KjG8ydENFtiZ4P', 'YFjiW3CMX7Z1Pq164lgbzKrm'))
        try:
            status=client.utility.verify_payment_signature(param_dict) #to check the authenticityof razorypay signature
            print(status)

            ord=Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id=response['razorpay_payment_id']
            ord.paid=True  #edit paid to true
            ord.save()

            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)

            #filterthe order_table details for particular user with order_id
            o=Order_table.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status='paid' #edit payment status=True
                i.save()
            c.delete()
            return render(request,'payment_status.html',{'status':True})
        except:
            return render(request,'payment_status.html',{'status':False})

    return render(request,'payment_status.html')



@login_required
def order_view(request):
    u=request.user
    orders=Order_table.objects.filter(user=u,payment_status='paid')
    return render(request,'orderview.html',{'orders':orders,'u':u.username})