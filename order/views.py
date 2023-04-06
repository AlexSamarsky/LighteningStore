from django.shortcuts import render, redirect
from order.models import * 
from order.forms import * 
from home.models import *
from product.models import *
from user.models import *
from django.contrib.auth.decorators import login_required
import json
from django.utils.crypto import get_random_string

# İyzico ödeme işlemleri için gerekli İmportlar


import iyzipay
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests

api_key = 'sandbox-lsk6KUGXAVNlm4RlO5xHF1iRswAgqatz'
secret_key = 'zyJW4yAuPfXw6npQ79WtB6p1sW96Lm82'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key':api_key,
    'secret_key':secret_key,
    'base_url':base_url
}

sozlukToken = list()


def payment(request):
    context = dict()
    profile = UserProfile.objects.get(id=request.user.id)
    zipcode = get_random_string(5).upper()
    adres= AddressModel.objects.get(customer=request.user.id)
    products = CartModel.objects.filter(customer=request.user)
    total = 0
    for product_ in products:
        total += product_.product.productPrice * product_.amount
    print(adres)
    buyer={
        'id': profile.id,
        'name': profile.first_name,
        'surname': profile.last_name,
        'gsmNumber': profile.phone,
        'email': profile.email,
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': adres.addressTitle,
        'ip': '85.34.78.112',
        'city': adres.addressCity,
        'country': adres.addressCountry,
        'zipCode': zipcode
    }

    address={
        'contactName': profile.first_name,
        'city': adres.addressCity,
        'country': adres.addressCountry,
        'address': adres.addressText,
        'zipCode': zipcode
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Bionlcular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]

    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice':total,
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        "callbackUrl": "http://127.0.0.1:8000/order/result/",
        "enabledInstallments": ['2', '3', '6', '9'],
        'buyer': buyer,
        'shippingAddress':address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    print(json_content["checkoutFormContent"]) # yukarıda girilen bilgiler boş ise checkoutFormContent hatası verir
    print("************************")
    print(json_content["token"])
    print("************************")
    sozlukToken.append(json_content["token"])
    return HttpResponse(f'<div id="iyzipay-checkout-form" class="responsive">{json_content["checkoutFormContent"]}</div>')


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda 
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)

@login_required(login_url='login')
def success(request):
    orderItems = CartModel.objects.filter(customer_id=request.user.id)
    # Ek giriş kontrolü
    if not orderItems:
        return redirect("login")
    ORDER      = OrderModel.objects.create(customer_id=request.user.id,complete=False)
    ORDER.save()
    for item in orderItems:
        ITEM=OrderItemModel.objects.create(product_id=item.product.id,quantity=item.amount,order_id=ORDER.id)
        ITEM.save()
    orderItems.delete()
    messages.success(request, 'Ödeme Başarılı')
    return redirect("completed")
    
def fail(request):
    messages.warning(request, 'Ödeme Başarısız')
    return redirect('checkout')

@login_required(login_url='login')
def completed(request):
    return render(request,"completed.html")

@login_required(login_url='login')
def v_myOrders(request):
    setting = Setting.objects.get(pk=1)
    customerOrders=OrderModel.objects.filter(customer_id=request.user.id)
    order = OrderItemModel.objects.filter(product_id=request.user.id)
    print(order)
    return render(request,"orders.html",{"customerOrderList":customerOrders, 'setting':setting})

