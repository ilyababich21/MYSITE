# Generated by Django 4.0.3 on 2022-05-11 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0005_rename_first_name_order_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='username',
        ),
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
