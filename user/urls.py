from django.urls import path
from user.views import *
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # path('register/', RegisterUser.as_view(), name='signup'),
    # path('login/', LoginView.as_view(template_name="login.html",authentication_form=UserLoginForm),name='login'),
    # path('logout/', logout_view, name='logout'),
    path('update/', user_update, name='user_update'),
    # path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    # path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    # path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='change_password/password_reset_confirm.html'),name='password_reset_confirm'),
    # path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='change_password/password_reset_complete.html'),
    # name='password_reset_complete'),
    path("sepetim/",views.v_cart,name="shoppingcart"),
    path("checkout/",views.v_checkout,name="checkout"),
    path("favorilerim/",views.v_favorites,name="favories"),
    path("profile/",views.v_profile,name="profile"),
    path("userDelete/",userDelete,name="userdelete"),
    path("adressDelete/",adressDelete,name="adressDelete"),
    path("update_item/",views.f_update_item,name="update_item"),
    path("update-cart/",views.f_update_cart,name="update-cart"),
    path("update-favorites/",views.f_update_favorites,name="update-favorites"),
]