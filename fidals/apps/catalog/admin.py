from django.contrib import admin
from .models import Category, Product

# Register your models here.


class MembershipInline(admin.TabularInline):
    model = Product.categories.through


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline
    ]
    exclude = ('categories',)


class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline
    ]
    list_display = ('id', 'name')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

