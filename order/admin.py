from django.contrib import admin
from order.models import *
# Register your models here.
admin.site.register(OrderItemModel)
admin.site.register(OrderModel)

    # if 'total' in request.POST:
    #     total = request.POST['total']
    #     paid = ShopCart.objects.filter(user_id=current_user.id)

    #     if Order.objects.filter(user_id=current_user.id, is_it_paid=False).exists():
    #         pay = Order.objects.get(user_id=current_user.id, is_it_paid=False)
    #         pay.total = total
    #         pay.shopcart.add(*paid)
    #         pay.save()
    #         return redirect('payment')
    #     else: 
    #         pay= Order.objects.create(
    #             user = request.user,
    #             total = total,
    #         )
    #         pay.shopcart.add(*paid)
    #         pay.save()
    #         return redirect('payment')