

from django.shortcuts import render
from django.views import View
from shop.models import Category
# Create your views here.
class Categoryview(View):
    def get(self,request):
        c=Category.objects.all()
        print(c)
        context={'categories':c}
        return render(request,'categories.html',context)

class Productview(View):
    def get(self, request, i):
        c = Category.objects.get(id=i)
        context = {'categories': c}
        return render(request, 'products.html', context)

