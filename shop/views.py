import datetime

import xlwt
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q
from django.http import FileResponse,HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter



def game_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    lines = []
    games = Product.objects.all()
    for game in games:
        lines.append(game.name)
        lines.append(game.category.name)
        lines.append(str(game.created))
        lines.append(str(game.price))

        lines.append(" ")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='games.pdf')


def export_doc(request):
    response=HttpResponse(content_type="text/")
    response['Content-Disposition'] = 'attachment; filename=products.doc'
    lines=[]
    products=Product.objects.all()
    for product in products:
        lines.append(f'{product.name}\n')
        lines.append(f'{product.price}\n')
        lines.append(f'{product.description}\n')

    response.writelines(lines)
    return response

def product_list(request, category_slug=None):
    search_querry=request.GET.get('search','')
    sort = request.GET.getlist('sort2')
    print(sort)
    category = None
    categories = Category.objects.all()
    if sort:
        products=Product.objects.filter(available=True).order_by(*sort)
    else:
        products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    if search_querry:
        products=products.filter(Q(name__icontains=search_querry)|Q(description__icontains=search_querry))
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})



def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug,available=True)
    cart_product_form=CartAddProductForm()
    return render(request, 'shop/product/detail.html',{'product':product,
                                                       'cart_product_form':cart_product_form})
