from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image_url', 'discount')
    search_fields = ('name',)
    fields = ('name', 'price', 'description', 'image_url', 'discount')
