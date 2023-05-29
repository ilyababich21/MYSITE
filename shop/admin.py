from django.contrib import admin
from .models import Category, Product, Company, Critery


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']



admin.site.register(Company, CompanyAdmin)
class CriteryAdmin(admin.ModelAdmin):
    list_display = ['name', 'pora_goda','vremya_sutok','vid_meropriatia']



admin.site.register(Critery, CriteryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'company','slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(Product, ProductAdmin)
