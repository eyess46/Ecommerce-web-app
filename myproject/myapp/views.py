from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import uuid
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import User
from django.contrib import messages
from django.contrib.auth.models import auth

# Create your views here.

def index(request):

	products = Product.objects.all().order_by("?")
	
	categories = Category.objects.all().order_by("?")
	
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		orderItems = order.orderitem_set.all()
	else:
		customer = "AnonymousUser"
		order  = {"cart_total": 0, "cart_price_total": 0}
		orderItems = []
		
	context = {
		"products": products,
		"order": order,
		"orderItems": orderItems,
		"categories": categories
	}
	return render(request, "index.html", context)

def about(request):

    return render(request, 'about.html') 

def contact(request):

    return render(request, 'contact.html') 


@login_required(login_url= "login")	
def cart(request):
	categories = Category.objects.all().order_by("?")
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		orderItems = order.orderitem_set.all()
	else:
		customer = "AnonymousUser"
		order  = {"cart_total": 0, "cart_price_total": 0}
		orderItems = []
		
	context = {
		"products": products,
		"order": order,
		"orderItems": orderItems,
		"categories": categories
	}
	return render(request, "cart.html", context) 



def products(request):
	
	products = Product.objects.all().order_by("?")
	
	categories = Category.objects.all().order_by("?")
	
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		orderItems = order.orderitem_set.all()
	else:
		customer = "AnonymousUser"
		order  = ""
		orderItems = {}
		
	context = {
		"products": products,
		"categories": categories,
		"order": order,
		"orderItems": orderItems
	}
	return render(request, "products.html", context)

def register(request):
	if request.method == "POST":
		email = request.POST.get("email")
		username = request.POST.get("username")
		first_name = request.POST.get("fName")
		last_name = request.POST.get("lName")
		password1 = request.POST.get("password1")
		password2 = request.POST.get("password2")
		
		if password1 == password2:
			if User.objects.filter(email= email).exists():
				messages.error(request, "Email already in use")
				return redirect("register")
			else:
				user = User.objects.create_user(
					username = username,
					email = email,
					password = password1,
					first_name = first_name,
					last_name = last_name
				)
				user.save()
				auth.login(request, user)
				return redirect("login")
		else:
			messages.error(request, "Passwords do not match")
			return redirect("register.html")
		
	return render(request, "register.html")

def logout(request):
	auth.logout(request)
	return redirect("/")
		
@login_required(login_url= "login")
def wishlist(request):
	categories = Category.objects.all().order_by("?")
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		orderItems = order.orderitem_set.all()
	else:
		customer = "AnonymousUser"
		order  = {"wishlist_total": 0, "wishlist_price_total": 0}
		orderItems = []
		
	context = {
		"products": products,
		"order": order,
		"orderItems": orderItems,
		"categories": categories
	}
	return render(request, "cart.html", context)   


@login_required(login_url= "login")
def checkout(request):
	
	categories = Category.objects.all().order_by("?")
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		orderItems = order.orderitem_set.all()
	else:
		customer = "AnonymousUser"
		order  = {"cart_total": 0, "cart_price_total": 0}
		orderItems = []
		
	context = {
		"products": products,
		"order": order,
		"orderItems": orderItems,
		"categories": categories
	}
	return render(request, "checkout.html", context)



def update_cart(request):
	response = json.loads(request.body)
	product_id = response["productId"]
	action = response["action"]
	
	print(product_id, action)
	
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		orderItem, created = OrderItem.objects.get_or_create(order= order, products_id= product_id)
		
		if action == "add":
			orderItem.quantity = orderItem.quantity + 1		
			orderItem.save()			
			
		if action == "remove":
			orderItem.delete()
			return redirect("cart.html")
	
	return JsonResponse("Item was added", safe= False)



def getCartTotal(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		product_total = order.cart_total
	else:
		order = {"cart_total": 0}
		customer = "AnonymousUser"
		product_total = order["cart_total"]
		
	data = product_total
		
	return JsonResponse(data, safe= False)
	


def getShippingData(request):
	response = json.loads(request.body)
	transaction_id = uuid.uuid4()
	price_total = response.get("price_total")
	
	address = response.get("address")
	city = response.get("city")
	country = response.get("country")
	zipcode = response.get("zipcode")
	telephone = response.get("telephone")
	
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer= customer, complete= False)
		order.transaction_id = transaction_id
		
		if str(order.cart_price_total) == price_total:		
			order.complete = True
			
		order.save()
		
		ShippingInfo.objects.create(
			customer= customer,
			order= order,
			address= address,
			city= city,
			country= country,
			zipcode= zipcode,
			telephone= telephone
		)
		
	return JsonResponse("Payment Successful", safe= False)	       

        


