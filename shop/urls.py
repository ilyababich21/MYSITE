from django.urls import re_path, path
from . import views

app_name = 'shop'

urlpatterns = [

    path('game_pdf', views.game_pdf, name='game_pdf'),
    path('export_doc', views.export_doc, name='export_doc'),
    re_path(r'^(?P<category_slug>[-\w]+)/$',
            views.product_list,
            name='product_list_by_category'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
            views.product_detail,
            name='product_detail'),
    re_path(r'^$', views.product_list, name='product_list'),

]
