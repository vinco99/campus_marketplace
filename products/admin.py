from django.contrib import admin
from .models import Category, Product, ProductImage

# Register your models here.
admin.site.register(Category)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]