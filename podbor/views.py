from django.http import HttpResponse
from django.shortcuts import render

from podbor.forms import PodborForm
from shop.models import Product, Critery, Category


# Create your views here.
def podbor_detail(request):
    if request.method == "POST":
        name = request.POST.get("languages")
        print(name)
        age = request.POST.get("vrem")
        print(age)
        vid_meropriatia = request.POST.get("vid")
        print(vid_meropriatia)
        criterys=Critery.objects.filter(pora_goda=name,vremya_sutok=age,vid_meropriatia=vid_meropriatia)
        print(criterys)
        crit=[crite.id for crite in criterys]
        print(crit)
        products = Product.objects.filter(available=True,critery__in=crit)
        print(str(products)+'ebat')
        category=Category.objects.all()
        print(category)
        # crinzh=products.filter(category=category)
        list=[]
        for catar in category:
            list.append(products.filter(category=catar.id)[0:1])
        


        return  render(request, "podbors/list.html", {'products': products})
    else:
        userform = PodborForm()
        return render(request, "podbors/index.html", {"form": userform})
