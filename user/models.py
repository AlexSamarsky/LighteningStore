from django.db import models
from django.contrib.auth.models import AbstractUser
from product.models import *
# Create your models here.

class UserProfile(AbstractUser): # Profil
    phone = models.CharField(max_length=50, verbose_name='Telefon No')
    profile_image = models.ImageField(null=True, blank=True, upload_to='image/users/' , verbose_name='Profil Resmi Ekle')

    class Meta:
        db_table = 'Kullanıcı_işlemleri'
        verbose_name = 'Kullanıcı_işlemleri'
        verbose_name_plural = 'Kullanıcı_işlemleri'

    def __str__(self):
        return self.username

    def user_name(self):
        return ' ' +self.first_name+ '  ' +self.last_name+ ' ['+self.username + '] ' +self.phone

class AddressModel(models.Model): # Adresler
    customer = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE,related_name="addres")
    addressTitle = models.CharField(max_length=50, verbose_name='Bölge')
    addressText = models.TextField(verbose_name="Adres Detayı", max_length=1000, null=False, blank=False)
    addressCity = models.CharField(max_length=100, verbose_name="Şehir")
    addressCountry = models.CharField(verbose_name="Ülke", max_length=50, null=False, blank=False)

    def __str__(self):
        return self.addressCountry
    class Meta:
        db_table = 'Address'
        verbose_name_plural="Adresler"


class FavoriteModel(models.Model): # Favoriler
    customer = models.ForeignKey('user.UserProfile', on_delete=models.CASCADE, verbose_name="Müşteri", related_name="customers")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Ürün", related_name="products")

    def __str__(self):
        return str(self.product)
    class Meta:
        db_table = 'Favorites'
        verbose_name_plural="Favoriler"

class CartModel(models.Model): # Sepet
    customer = models.ForeignKey('user.UserProfile', on_delete=models.SET_NULL, verbose_name="Müşteri", null=True, related_name="customerss")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, verbose_name="Ürün", null=True, related_name="productss")
    amount = models.IntegerField(verbose_name="Adet", null=False)

    def __str__(self):
        return str(self.product)
    class Meta:
        db_table = 'Cart'
        verbose_name_plural="Sepet"