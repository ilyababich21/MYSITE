from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Company(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    email = models.EmailField()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'

    def __str__(self):
        return self.name

class Critery(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    pora_goda = models.CharField(max_length=200, )
    vremya_sutok = models.CharField(max_length=200, )
    vid_meropriatia = models.CharField(max_length=200, )
    # name = models.CharField(max_length=200, db_index=True)
    # name = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Критерий'
        verbose_name_plural = 'Критерии'

    def __str__(self):
        return self.name+'  '+self.pora_goda+"   "+self.vid_meropriatia



class Product(models.Model):
    critery=models.ForeignKey(Critery, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
