from django.contrib import admin
from .models import Order, OrderItem
import csv
import xlwt
import datetime
from django.http import HttpResponse
from django.http import FileResponse

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


from django.http import HttpResponse
from django.core import serializers

def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'

def file_iterator(filename, chuck_size=512):
    """
         Вернуть файл по частям
         : param filename: имя файла
         : param chuck_size: Размер блока, по умолчанию 512
         : return: Файл возвращается блоками как повторяемый объект
    """
    with open(filename, "rb") as f:
        while True:
            c = f.read(chuck_size)
            if c:
                yield c
            else:
                break

def export_to_xls(queryset, headers, columns, filename='file_name'):
    """
         Создайте файл Excel с переданными данными и верните файл с возвратом потока данных
         : param queryset: Список данных, обычно отфильтрованный результат.
    :param headers:
                 Заголовок Excel передается в виде списка.
                 Например: ['ID', 'имя', 'номер телефона', 'изменение суммы', 'баланс после изменения']
    :param columns:
                 Имя столбца данных передается в виде списка.
                 Например: ['pk', 'customer__name', 'customer__mobile', 'amount', 'current_amounts'].
         : param filename: возвращает имя файла, оно должно иметь суффикс .xls
    :return:
    """
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("data")
    for i, h in enumerate(headers):
        sheet.write(0, i, h)
    cols = 1
    for query in queryset.values(*columns):
        for i, k in enumerate(columns):
            v = query.get(k)
            if isinstance(v, datetime.datetime):
                v = v.strftime('%Y-%m-%d %H:%M:%S')
            sheet.write(cols, i, v)
        cols += 1
    wb.save(filename)
    response = FileResponse(file_iterator(filename))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def save_execl(self, request, queryset):
        filename = 'media/{0}_{1}.xls'.format('amounts', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        headers = ['id', 'user','first_name', 'last_name', 'email',
                    'address', 'phone', 'city', 'paid',
                    'created', 'updated']
        columns = ['id', 'user', 'first_name','last_name', 'email',
                    'address', 'phone', 'city', 'paid',
                    'created', 'updated']
        return export_to_xls(queryset, headers, columns, filename)

save_execl.short_description = "Экспорт в Excel"

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name','last_name', 'email',
                    'address', 'phone', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv, save_execl,export_as_json]





admin.site.register(Order, OrderAdmin)