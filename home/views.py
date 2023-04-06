from django.shortcuts import render, redirect
from home.models import *
from home.forms import *
from product.models import *
from order.models import *
from django.views.generic.edit import FormView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

FAKE_DB_CAROUSEL =[
    f"https://picsum.photos/id/{id}/1000/500" for id in range(0, 3)
]


def index(request):
    setting = Setting.objects.get(pk=1)

    category_list = Category.objects.all().order_by('id')[:3]
    global_categories = Category.objects.filter(id__range =(16,100))
    home_categories_left = Category.objects.filter(id='63')
    home_categories_right = Category.objects.filter(id='64')
    home_categories_center = Category.objects.filter(id__range =(65,66))

    # images = Images.objects.all()

    super_deals = Product.objects.all().order_by('-id') # Süper fırsatlar

    just_came_all = Product.objects.all().order_by('?')
    just_came_women = Product.objects.filter(productCategorie__title =('Kadın Giyim & Aksesuar')) # Detay Sayfasında da ilgili ürünleri göstermek için bunları Kullanabilirsin
    just_came_man = Product.objects.filter(productCategorie__title =('Erkek Giyim & Aksesuar'))
    just_came_child = Product.objects.filter(productCategorie__title =('Çocuk Giyim & Aksesuar'))

    trending_products_all = Product.objects.all().order_by('?')
    trending_products_computer = Product.objects.filter(productCategorie__title =('Bilgisayar'))
    trending_products_electronic = Product.objects.filter(productCategorie__title =('Elektronik'))
    trending_products_decor = Product.objects.filter(productCategorie__title =('Dekorasyon & Aydınlatma'))

    populer_products = Product.objects.filter(id__range =(64,85))
    special_offer = Product.objects.all().order_by('-id')[:2]

    campaigns = Campaigns.objects.filter(id__range =(4,12))
    campaigns1 = Campaigns.objects.filter(id__range =(1,3))
    campaigns2 = Campaigns.objects.filter(id__range =(13,25))

    favorites = FavoriteModel.objects.filter(customer=request.user.id)
    products = CartModel.objects.filter(customer=request.user.id)
    total = 0
    for product_ in products:
        total += product_.amount * product_.product.productPrice
    request.session['cart_items'] = CartModel.objects.filter(customer_id=request.user.id).count()
    request.session['favories_items'] = FavoriteModel.objects.filter(customer_id=request.user.id).count()
    context = dict(
        setting = setting,
        category_list = category_list,
        global_categories = global_categories,
        campaigns1 = campaigns1,

        just_came_all = just_came_all,
        just_came_women = just_came_women,
        just_came_man = just_came_man,
        just_came_child = just_came_child,

        trending_products_all = trending_products_all,
        trending_products_computer = trending_products_computer,
        trending_products_electronic = trending_products_electronic,
        trending_products_decor = trending_products_decor,

        special_offer = special_offer,
        campaigns = campaigns,
        campaigns2=campaigns2,
        populer_products = populer_products,
        super_deals = super_deals,
        FAKE_DB_CAROUSEL = FAKE_DB_CAROUSEL,
        products = products,
        total = total,
        favorites = favorites,
        home_categories_left = home_categories_left,
        home_categories_right = home_categories_right,
        home_categories_center = home_categories_center,
        # images = images,
    )
    return render(request, 'index.html', context)

class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/submit/'

    def form_valid(self, form):
        name = form.cleaned_data['name']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        email = form.cleaned_data['email']

        mail = EmailMessage(
            f'{name}, Tarafından Mesaj Gönderildi',
            f'Konu: {subject}\n\nEmail: {email}\n\nMesaj: {message}\n\n',
            f'"YENİ MESAJ" <{email}>',
            [settings.EMAIL_ADMIN], 
                reply_to=[f'{email}'], 
        )
        mail.send()
        form.save()
        messages.success(self.request, 'Mesajınız başarıyla gönderildi.')
        return super().form_valid(form)


def referance(request):
    setting = Setting.objects.get(pk=1)
    global_categories = Category.objects.filter(id__range =(16,30))
    return render(request, 'referance.html', context={
        'setting': setting,
        'category_list': global_categories,
        })


def about(request):
    setting = Setting.objects.get(pk=1)
    return render(request, 'about.html', context={
        'setting': setting,
        })

# Search
def search_product(request):
    setting = Setting.objects.get(pk=1)
    products = Product.objects.all()
    query = ''
    if request.method == 'GET':
        query = request.GET.get('query')
        products = products.filter(
            Q(productTitle__icontains=query) |
            Q(productCategorie__title__icontains=query) |
            Q(productDescription__icontains=query)
            ).distinct()
    return render(request, 'search.html', context={
        'products':products,
        'query':query,
        'setting':setting
    })