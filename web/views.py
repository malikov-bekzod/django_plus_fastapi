from django.shortcuts import render
from django.views import View
from .models import Product

class HomeView(View):
    def get(self,request):
        products = Product.objects.all()
        context = {
            "products":products
        }
        return render(request, "web/base.html",context)