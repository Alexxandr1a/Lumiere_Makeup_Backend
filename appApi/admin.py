from django.contrib import admin
from .models import Cart, CartItem, Category, Product, CustomUser, ProductRating, Review
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name")
admin.site.register(CustomUser, CustomUserAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "featured")
    list_filter = ("category", "featured")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)} 
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
       list_display = ("name", "slug")
       prepopulated_fields = {"slug": ("name",)}
       search_fields = ("name",)
admin.site.register(Category, CategoryAdmin)

admin.site.register([Cart, CartItem, Review, ProductRating])