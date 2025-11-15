

from django.shortcuts import render,redirect
from django.views import View
from shop.models import Category,Product
from shop.forms import SignupForm, LoginForm
from django.contrib import messages

# Create your views here.
class Categoryview(View):
    def get(self,request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request,'categories.html',context)

class Productview(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'categories': c}
        return render(request,'products.html',context)

class ProductDetailview(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'products': p}
        return render(request,'productdetail.html',context)


class Register(View):
    def post(self, request):
        print(request.POST)
        form_instance=SignupForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:userlogin')
        else:
            print('error')
            return render(request, 'register.html', {'form': form_instance})

    def get(self, request):
        form_instance=SignupForm()
        context={'form': form_instance}
        return render(request, 'register.html', context)


from django.contrib.auth import login, authenticate, logout

class Userloginview(View):
    def post(self, request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            u = form_instance.cleaned_data['username']
            p = form_instance.cleaned_data['password']
            user = authenticate(username=u, password=p)

            if user and user.is_superuser == True:
                login(request, user)
                return redirect('shop:categories')

            elif user and not user.is_superuser:  # 👈 normal user condition
                login(request, user)
                return redirect('shop:categories')

            else:
                messages.error(request, 'invalid user credentials')
                return render(request, 'userlogin.html', {'form': form_instance})
        else:
            messages.error(request, 'invalid user credentials')
            return render(request, 'userlogin.html', {'form': form_instance})

    def get(self, request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, 'userlogin.html', context)



class Userlogoutview(View):
    def get(self, request):
        logout(request)
        return render(request, 'userlogout.html')

from shop.forms import CategoryForm,ProductForm,StockForm

class AddcategoryView(View):
    def post(self, request):
        form_instance = CategoryForm(request.POST, request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
        else:
            print('error')
            return render(request, 'addcategory.html', {'form': form_instance})

    def get(self, request):
        form_instance = CategoryForm()
        context = {'form': form_instance}
        return render(request, 'addcategory.html', context)

class AddproductView(View):
    def post(self, request):
        form_instance=ProductForm (request.POST, request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
        else:
            print('error')
            return render (request,'addproduct.html',{'form': form_instance})
    def get(self, request):
        form_instance=ProductForm()
        context={'form':form_instance}
        return render (request,'addproduct.html',context)


class AddstockView(View):
    def post(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=StockForm(request.POST,instance=p)

        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
        else:
            print('error')
            return render (request,'addstock.html',{'form': form_instance})

    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=StockForm(instance=p)
        context={'form': form_instance}
        return render (request,'addstock.html',context)