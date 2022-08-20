from django.contrib import admin
from .models import Category, Product, ContactForm
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price','available']
    prepopulated_fields = {'slug':('name',)}

@admin.register(ContactForm)
class CustomContactAdmin(admin.ModelAdmin):
    list_display = ['name','email', 'subject']
    list_filter = ['message', 'subject']
