from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path("", views.home, name="home"),
   path("product_list/", views.product_list, name='product_list'),
   path("product_details/<slug>", views.product_details, name='product_details'),
   path("about/", views.about,name='about'),
   path("check-out/<slug>",views.checkout, name="check-out"),
   path("transaction_success/", views.transaction_success, name="transaction_success"),
   path("testimonial/", views.testimonial, name='testimonial'),
   path("contact/", views.contact, name="contact"),
   path("contact-form/", views.contactForm, name="contact-form"),
   path("blog/", views.blog, name="blog"),


   # Account Login
   path("signup/", views.signup, name="signup"),
   path("accounts/", include('django.contrib.auth.urls')), # make sure its on single ' '

   path("user_profile/", views.user_profile, name="user_profile"),
   path("update_profile/<id>/", views.update_profile,name="update_profile"),

   # Django cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)