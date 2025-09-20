from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (
    Product, Attribute, AttributeValue, ProductVariant, Category, Wishlist
)

class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]
    list_display = ('name',)

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    filter_horizontal = ('attributes',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    inlines = [ProductVariantInline]
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent', 'total_products_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


admin.site.register(Wishlist)