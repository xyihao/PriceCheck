from django.contrib import admin
from models import Products
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
	list_display=('name','rsp','price','site','store','datetime')
	ordering=('site','name','datetime',)

admin.site.register(Products, ProductAdmin)
