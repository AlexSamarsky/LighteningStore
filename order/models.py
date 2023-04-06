from django.db import models
from product.models import *
from user.models import *
from unidecode import unidecode
from django.template.defaultfilters import slugify
import random, string


class OrderModel(models.Model): # sipariş veren kişi bilgisi
    customer = models.ForeignKey('user.UserProfile', on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name="Müşteri", related_name="customersss")
    complete = models.BooleanField(default=False, null=True, blank=False, verbose_name="Tamamlandı mı")
    orderAddress = models.ForeignKey(AddressModel, null=True, blank=False, on_delete=models.SET_NULL,
                                     verbose_name="Sipariş Adresi" , related_name="orderaddress")
    # transaction_id = models.CharField(max_length=200, null=True, verbose_name="İşlem Numarası")
    slug = models.SlugField(null=True, unique=True, editable=True)
    first_name = models.CharField(max_length=10, verbose_name='İsim') 
    last_name = models.CharField(max_length=10, verbose_name='Soyisim')  
    phone = models.CharField(blank=True, max_length=20, verbose_name='Telefon No')
    address = models.CharField(blank=True, max_length=150, verbose_name='İlçe')
    city = models.CharField(blank=True, max_length=20, verbose_name='Şehir')
    country = models.CharField(blank=True, max_length=20, verbose_name='Ülke')
    email = models.EmailField()
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(max_length=100, default='Beklemede')
    date_order = models.DateTimeField(auto_now_add=True, verbose_name="Sipariş Tarihi")

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            title = str(self.customer.username) + "-"
            title = slugify(unidecode(title))
            self.slug = slugify(unidecode(title)) + ''.join(
                random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20))
        super(OrderModel, self).save()

    def __str__(self):
        return str(self.id) + " " + self.customer.username

    class Meta:
        db_table = 'Orders'
        verbose_name_plural = "Siparişler"

class OrderItemModel(models.Model): # Sipariş verilen ürünün bilgileri
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name="Ürün", related_name="products2")
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, null=True, verbose_name="Sipariş", related_name="orders")
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Adet")
    create_att = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        db_table = 'Order_Items'
        verbose_name_plural = "Sipariş Ürünleri"
