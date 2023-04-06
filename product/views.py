from django.shortcuts import render, get_object_or_404, redirect
from home.models import *
from product.models import *
from product.forms import *
from user.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
# Create your views here.

def category_products(request, slug):
    product = Product.objects.filter(productCategorie__slug = slug).order_by('id')
    # numbers_list = range(1, 20)
    page = request.GET.get('page')
    paginator = Paginator(product, 3)  
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)
    
    global_categories = Category.objects.filter(id__range =(16,100))
    setting = Setting.objects.get(pk=1) 
    # döngü kullanmaya gerek kalmasın diye slug ile gelen kategoriyi get ile getiriyoruz
    kategori = Category.objects.get(slug=slug)
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(customer=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'categories.html', context={
        'setting':setting,
        'product':product,
        'kategori':kategori,
        'global_categories':global_categories,
        'favorites':favorites,
        'products':products,
        'total':total,
        # 'numbers': numbers
    })
def campaigns_products(request, slug):
    product = Product.objects.filter(productCampaigns__slug = slug).filter(id__range=(1, 16)) # toplam 16  tane liste 
    page = request.GET.get('page', 1)
    paginator = Paginator(product, 4)  # sayfa başına 4 sayı blokları
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    global_categories = Category.objects.filter(id__range =(16,100))
    setting = Setting.objects.get(pk=1) 
    # product = Product.objects.filter(productCampaigns__slug = slug) 
    campaigns = Campaigns.objects.get(slug=slug)
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(customer=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'campaigns.html', context={
        'setting':setting,
        'product':product,
        'campaigns':campaigns,
        'global_categories':global_categories,
        'favorites':favorites,
        'products':products,
        'total':total,
        'numbers': numbers
    })


def detail(request, id, slug):
    setting = Setting.objects.get(pk=1) 
    product = Product.objects.get(pk=id)
    global_categories = Category.objects.filter(id__range =(16,100))
    popular_products = Product.objects.all().order_by('id')[:2]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    relevant_product = Product.objects.all()[:20]

    random_products = Product.objects.all().order_by('?')[:8]
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(customer=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'detail.html', context={
        'setting':setting,
        'product':product,
        'images':images,
        'comments':comments,
        'relevant_product':relevant_product,
        'popular_products':popular_products,
        'favorites':favorites,
        'products':products,
        'total':total,
        'global_categories':global_categories,
        'random_products':random_products,
    })

def campaigns_detail(request, id, slug):
    setting = Setting.objects.get(pk=1) 
    product = Product.objects.get(pk=id)
    global_categories = Category.objects.filter(id__range =(16,100))
    popular_products = Product.objects.all().order_by('id')[:2]
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    relevant_product = Product.objects.all()[:20]

    random_products = Product.objects.all().order_by('?')[:8]
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(customer=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'campaigns_detail.html', context={
        'setting':setting,
        'product':product,
        'images':images,
        'comments':comments,
        'relevant_product':relevant_product,
        'popular_products':popular_products,
        'favorites':favorites,
        'products':products,
        'total':total,
        'global_categories':global_categories,
        'random_products':random_products,
    })


@login_required(login_url='login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user  
            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Yorumunuz Başarıyla Gönderilmiştir! Teşekkür Ederiz.')
            
            return HttpResponseRedirect(url)
    messages.warning(request, 'Yorum Yaparken Bir Sorunn Oluştu Lütfen Tekrar Deneyin.')
    return HttpResponseRedirect(url)   

@login_required(login_url='login')
def comments(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(customer=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return render(request, 'coments.html', context={
        'comments':comments,
        'setting':setting,
        'favorites':favorites,
        'products':products,
        'total':total,
    })
