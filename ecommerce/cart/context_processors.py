from .models import Cart


def total(requset):
    u=requset.user
    count=0

    if requset.user.is_authenticated:
        try:
            item=Cart.objects.filter(user=u)
            count=item.count()
        except:
            count=0
    return {'count':count}