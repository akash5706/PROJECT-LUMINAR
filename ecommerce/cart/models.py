from django.db import models
from shop.models import Product
from django.contrib.auth.models import User
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_added=models.DateTimeField(auto_now_add=True)
    def _str_(self):
        return self.user.username

    def subtotal(self):      #self means current card object
        return self.product.price*self.quantity

class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField(null=True)
    order_id=models.CharField(max_length=100)
    ordered_date=models.DateTimeField(auto_now=True)
    phone=models.IntegerField()
    address=models.TextField()
    is_ordered=models.BooleanField(default=False)
    payment_method=models.CharField(max_length=50)
    delivery_status=models.CharField(max_length=50, default="pending")
    def _str_(self):
        return self.user.username


class Order_items(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="products")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    def _str_(self):
        return self.product.name