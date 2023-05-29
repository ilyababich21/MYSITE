from django.urls import re_path
from podbor import views

app_name = 'podbor'

urlpatterns = [
    re_path(r'^$', views.podbor_detail, name='podbor_detail'),

]
