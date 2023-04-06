from django.urls import path
from order.views import *

urlpatterns = [       
    path('payment/', payment, name='payment'),
    path('result/', result, name='result'),
    path('success/', success, name='success'),
    path('failure/', fail, name='failure'),
    path("order/",v_myOrders,name="order"),
    path("completed/",completed,name="completed"),
]