from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from user.forms import *
from user.models import *
from order.models import *
from order.forms import *
from home.models import *
from product.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json
from django.utils.crypto import get_random_string

@login_required(login_url='login')
def v_profile(request):
    setting = Setting.objects.get(pk=1)
    user = UserProfile.objects.filter(id=request.user.id)
    profile = UserProfile.objects.get(id=request.user.id)
    userAddress = AddressModel.objects.filter(customer=request.user)
    adresForm= AddressForm(request.POST or None)
    if adresForm.is_valid():
        address = adresForm.save(commit=False)
        address.customer = request.user
        address.save()
        messages.success(request, "Address Başarıyla Eklendi")
        return redirect("profile")
    return render(request, "profile.html", {"user": user[0], "userAddress": userAddress,"adresForm": adresForm, 'profile':profile, 'setting':setting})

@login_required(login_url='login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance= request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'{request.user.username} Profiliniz başarıyla güncellendi.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance= request.user)
        profile_form= ProfileUpdateForm(instance= request.user) 
        current_user = request.user
        profile = UserProfile.objects.get(id=current_user.id)
        setting = Setting.objects.get(pk=1)
        return render(request, 'user_update.html', context={
            'profile_form':profile_form,
            'user_form':user_form,
            'profile':profile,
            'setting':setting
        })
    
def userDelete(request):
    profile = request.user
    profile.delete()
    messages.success(request, 'Hesabınız başarıyla silinmiştir.')
    return redirect('/')


def adressDelete(request):
    address = AddressModel.objects.filter(customer=request.user)
    address.customer = request.user
    address.delete()
    messages.success(request, "Address Başarıyla Silindi")
    return redirect('profile')


@login_required(login_url='login')
def v_favorites(request):
    setting = Setting.objects.get(pk=1)
    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    return render(request, "favories.html", {"favorites": favorites, 'setting':setting})

@login_required(login_url='login')
def v_cart(request):
    setting = Setting.objects.get(pk=1)
    products = CartModel.objects.filter(customer=request.user)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    return render(request, "shoppingcart.html", {"products": products, "total": total, 'setting':setting})


@login_required(login_url='login')
def v_checkout(request):
    zipcode = get_random_string(5).upper()
    setting = Setting.objects.get(pk=1)
    cartItems=CartModel.objects.filter(customer_id=request.user.id)
    if not cartItems:
        #eğer kullanıcının sepeti boşsa ve bu sayfaya gitmeye çalışıyorsa gelecek uyarı
        messages.warning(request, "önce sepetinize ürün eklemelisiniz Speteiniz Boş")
        return redirect("/")
    else:
        #eğer sepetinde ürün varsa bu sayfa açılacak
        # Address eklendiğinde çalışan blok
        form = OrderForm(request.POST or None)
        if form.is_valid():
            address = form.save(commit=False)
            address.addressCountry = form.cleaned_data.get("addressCountry")
            address.customer = request.user
            address.save()
            messages.success(request, "Address Başarıyla Eklendi")
            return redirect("checkout")
        # Address eklendiğinde çalışan blok
        customerAddress = AddressModel.objects.filter(customer=request.user)
        products = CartModel.objects.filter(customer=request.user)
        total = 0

        for product_ in products:
            total += product_.product.productPrice * product_.amount

        return render(request, "checkout.html",
                      {"products": products, "total": total, "form": form, "customerAddress": customerAddress, 'setting':setting, 'zipcode':zipcode})


@login_required(login_url='login')
def f_update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    _customer = request.user

    product = Product.objects.get(id=productId)
    cartItem = CartModel.objects.filter(customer=_customer).filter(product_id=productId)
    if not cartItem:
        cartItem = CartModel.objects.create(product_id=productId, customer=_customer, amount=1)
        cartItem.save()
        
    else:
        cartItem = CartModel.objects.get(customer=_customer, product_id=productId)
        if action == "add":
            cartItem.amount += 1
        elif action == "remove":
            cartItem.amount -= 1
        cartItem.save()
        request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
    return JsonResponse(
        "<div class='alert alert-success m-3 p-3 rounded'><i class='fa fa-check' aria-hidden='true'></i> Ürün Başarıyla Sepetinize Eklenmiştir</div>",
        safe=False)

@login_required(login_url='login')
def f_update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data["action"]
    cartItem = CartModel.objects.get(product_id=productId, customer_id=request.user.id)
    if action == "add":
        cartItem.amount += 1
        cartItem.save()
        request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
        messages.success(request, "Sepetiniz başarıyla güncellenmiştir")
    elif action == "remove":
        if cartItem.amount == 1:
            cartItem.delete()
            request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
            messages.success(request, "Ürün başarıyla sepetinizden kaldırılmıştır")
        else:
            cartItem.amount -= 1
            cartItem.save()
            request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
            messages.success(request, "Sepetiniz başarıyla güncellenmiştir")

    return JsonResponse("asdf", safe=False)

@login_required(login_url='login')
def f_update_favorites(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data["action"] 
    if action == "add":
        try:
            # eğer ürünü veritabanında bulursa try blogu calısacak
            favItem = FavoriteModel.objects.get(customer_id=request.user.id, product_id=productId)
            return JsonResponse(
                "<div class='alert alert-danger m-3 p-3 rounded'><i class='fa fa-check' aria-hidden='true'></i> Ürün zaten favorilerinizdedir</div>",
                safe=False)
        except:
            # ürünü bulamazsa except kısmı çalışarak veritabanına favori kaydediyor.
            newFavItem = FavoriteModel.objects.create(customer_id=request.user.id, product_id=productId)
            newFavItem.save()
            request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
            return JsonResponse(
                "<div class='alert alert-success m-3 p-3 rounded'><i class='fa fa-check' aria-hidden='true'></i> Ürün başarıyla favorilerinize eklenmiştir.</div>",
                safe=False)

    elif action == "remove":
        favItem = FavoriteModel.objects.get(customer_id=request.user.id, product_id=productId)
        favItem.delete()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    return JsonResponse(
        "<div class='alert alert-success m-3 p-3 rounded'><i class='fa fa-check' aria-hidden='true'></i> Ürün Başarıyla Favorilerinizden Kaldırılmıştır</div>",
        safe=False)


# @login_required(login_url='login')
# def profile(request):
#     setting = Setting.objects.get(pk=1)
#     current_user = request.user
#     profile = UserProfile.objects.get(id=current_user.id)
#     return render(request, 'profile.html', context={
#         'setting':setting,
#         'profile':profile
#     })





