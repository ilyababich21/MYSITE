# Generated by Django 4.0.3 on 2022-05-12 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_company_product_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='company',
        ),
    ]