from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views import View
from cart.models import Cart
from shop.models import Product
from django.contrib import messages
import razorpay



class AddtoCart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p) #checks whether the product is already placed by the user
            c.quantity+=1                        #or checks whether the product is there in the cart table
            c.save()                             #if yes then increment quantity by 1
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)   #else creates a new cart record insisde cart tabel
            c.save()
        return redirect('cart:cartview')

class Cartview(View):
    def get(self, request):
        u=request.user
        c=Cart.objects.filter(user=u)#filters the cart items selected by current user
        total=0
        for i in c:
            total+=i.product.price*i.quantity
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)
class Minuscart(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()
        except:
            pass

        return redirect('cart:cartview')


class Deletecart(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            c.delete()
        except:
            pass

        return redirect('cart:cartview')

from cart.forms import OrderForm

def checkstock(c):
    stock=True
    for i in c:
        if i.product.stock<i.quantity:
            stock = False
            break
    else:
        stock = True
    return stock
import uuid
class Checkout(View):
    def post(self, request):
        form_instance = OrderForm(request.POST)
        if form_instance.is_valid():
            o = form_instance.save(commit=False)
            u = request.user  # current user
            o.user = u
            c = Cart.objects.filter(user=u)
            total = 0
            for i in c:
                total += i.product.price * i.quantity
            o.amount = total
            o.save()

            if o.payment_method == "online":
                # Razorpay client connection
                client = razorpay.Client(auth=('rzp_test_Rf74oI0rwzOQRG', 'hJk8SVjxMhbHS8N9f4AUEygr'))
                response_payment = client.order.create(dict(amount=total * 100, currency='INR'))
                o.order_id = response_payment['id']
                o.save()

                context = {'payment': response_payment}
                return render(request, 'payment.html', context)

            else:  # order COD
                o.is_ordered = True
                uid = uuid.uuid4().hex[:14]
                o.order_id = 'order_COD' + uid
                o.save()

                for i in c:
                    items = Order_items.objects.create(order=o, product=i.product, quantity=i.quantity)
                    items.product.stock -= items.quantity
                    items.product.save()
                    items.save()

                # clear cart
                c.delete()

                messages.success(request, "Order placed successfully (COD)")
                return render(request, 'payment.html')

        else:
            # form is invalid → return same page with errors
            messages.error(request, "Invalid order form! Please fill all required fields.")
            return render(request, 'checkoutform.html', {'form': form_instance})

    def get(self, request):
        u = request.user
        c = Cart.objects.filter(user=u)
        stock = checkstock(c)
        if stock:
            form_instance = OrderForm()
            context = {'form': form_instance}
            return render(request, 'checkoutform.html', context)
        else:
            messages.error(request, "Cannot place your order — some items are out of stock.")
            return render(request, 'checkoutform.html')








#after payment completion razorpay redirects into payment_success view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from cart.models import Order,Order_items

@method_decorator(csrf_exempt,name="dispatch")

class Payment_success(View):
    def post(self,request,i):                        #here i represents the username
        #to add current user into current session again
        u=User.objects.get(username=i)
        login(request,u)    #adds the user object u into session


        response=request.POST    #after payment razorpay sends payment details into success view as response
        print(response)

        id=response['razorpay_order_id']
        print(id)

        #order
        order=Order.objects.get(order_id=id)
        order.is_ordered=True  #after successful completion of order
        order.save()

        #order_items
        c=Cart.objects.filter(user=u)
        for i in c:
            o=Order_items.objects.create(order=order,product=i.product,quantity=i.quantity)
            o.save()
            o.product.stock-=o.quantity
            o.product.save()

        #cart deletion
        c.delete()

        return render(request,'payment_success.html')



class Orders(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}

        return render(request,'orders.html',context)