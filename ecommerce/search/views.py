from django.shortcuts import render

from shop.models import Product
from django.db.models import Q
def search_product(request):
    p=None
    qurey=''
    if(request.method=='POST'):
        query=request.POST['q']
        if query:
            p=Product.objects.filter(Q(name__icontains=query)|Q(desc__icontains=query))
            return render(request,'search.html',{'p':p})
