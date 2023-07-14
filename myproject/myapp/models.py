from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
	username = models.CharField(max_length= 100)
	email = models.EmailField(unique= True)
	first_name = models.CharField("First Name", max_length= 100)
	last_name = models.CharField("Last Name", max_length= 100)
	
	REQUIRED_FIELDS = ["username"]
	USERNAME_FIELD = "email"
	
	
	def _str_(self):
		return self.username
	
	
class Product(models.Model):
	name = models.CharField(max_length= 100)
	price = models.DecimalField(max_digits= 100, decimal_places= 2, default= 0)
	image = models.ImageField(upload_to= "images/")
	discount = models.DecimalField(max_digits= 4, decimal_places= 2)
	category = models.ForeignKey("Category", on_delete= models.SET_NULL, null= True, blank= True)
	
	
	def _str_(self):
		return self.name
		
		
class Category(models.Model):
	name = models.CharField(max_length= 30)
	
	def _str_(self):
		return self.name
		
	class Meta:
		verbose_name_plural = "Categories"
		
		
class Order(models.Model):
	customer = models.ForeignKey(User, on_delete= models.SET_NULL, null= True, blank= True)
	date_created = models.DateTimeField(auto_now= True)
	transaction_id = models.CharField(max_length= 100, null= True, blank= True)
	complete = models.BooleanField(default= False)
	transaction_id = models.CharField(max_length= 36)
	
	
	def _str_(self):
		return str(self.id)
		
	@property
	def cart_total(self):
		count = 0
		for item in self.orderitem_set.all():
			count += item.quantity
		return count
		
		
	@property
	def cart_price_total(self):
		total = 0
		for item in self.orderitem_set.all():
			total = (item.quantity * item.products.price) + total
		return total
	

		
		
		
class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete= models.SET_NULL, null= True, blank= True)
	products = models.ForeignKey(Product, on_delete= models.SET_NULL, null= True, blank= True)
	quantity = models.IntegerField(default= 0)
	
	
	@property
	def price_times_quantity(self):
		return self.products.price * self.quantity
	
	
class ShippingInfo(models.Model):
	customer = models.ForeignKey(User, on_delete= models.SET_NULL, null= True, blank= True)
	order = models.ForeignKey(Order, on_delete= models.SET_NULL, null= True, blank= True)
	country = models.CharField(max_length= 100, null= True)
	city = models.CharField(max_length= 100, null= True)
	address = models.CharField(max_length= 800, null= True)
	zipcode = models.CharField(max_length= 300)
	telephone = models.CharField(max_length= 15)
	
	def _str_(self):
		return self.country
		
		
	class Meta:
		verbose_name_plural = "ShippingInfo"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    		
