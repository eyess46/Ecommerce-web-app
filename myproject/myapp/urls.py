from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('wishlist', views.wishlist, name='wishlist'),
    path('products', views.products, name='products'),
    path('register', views.register, name='register'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),

    # JavaScript Links
	path("update_cart", views.update_cart, name= "update_cart"),
	path("getCartTotal", views.getCartTotal, name= "getCartTotal"),
	path("getShippingData", views.getShippingData, name= "getShippingData"),
    path("login", auth_views.LoginView.as_view(template_name="login.html"), name= "login"),
	path("register", views.register, name= "register"),
	path("logout", views.logout, name= "logout"),
    path('wishlist', views.wishlist, name='wishlist'), # For add to wishlist

    
    

]