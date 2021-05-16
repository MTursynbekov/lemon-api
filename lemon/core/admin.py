from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from core.models import Product, ProductImage, ProductSpecification, Category, Brand, City, Store, Promotion


class ProductImageInLine(admin.TabularInline):
    model = ProductImage


class ProductSpecificationInLine(admin.TabularInline):
    model = ProductSpecification


class CustomMPTTModelAdmin(MPTTModelAdmin):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'type')
    inlines = (ProductImageInLine, ProductSpecificationInLine)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')


admin.site.register(Category, CustomMPTTModelAdmin)
admin.site.register(Promotion)