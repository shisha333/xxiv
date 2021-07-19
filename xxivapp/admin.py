from django.contrib import admin
from .models import Payment,Stock,Product,Order,Discount,Taxes,Customer,CustomOrder
from django.db.models import Q
# Register your models here.
@admin.register(Payment)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content","created_at")
    search_fields = ("content","title", )
    list_filter = ("created_at", )

@admin.register(Stock)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("title", "content","created_at")
    search_fields = ("content","title", )
    list_filter = ("created_at", )
   


@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    list_display = ("name","brand_name","price","profit","created_at","updated_at")
    search_fields = ("name","brand_name", )
    list_filter = ("created_at", )

@admin.register(Order)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content","created_at")
    search_fields = ("content","title", )
    list_filter = ("created_at", )

@admin.register(Discount)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content","created_at")
    search_fields = ("content","title", )
    list_filter = ("created_at", )

@admin.register(Taxes)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content","created_at")
    search_fields = ("content","title", )
    list_filter = ("created_at", )

@admin.register(Customer)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "content","created_at")
    search_fields = ("content","title", )
    list_filter = ("created_at", )

@admin.register(CustomOrder)
class CustomOrderAdmin(admin.ModelAdmin):
    list_display = [ "title","name", "email", "phone"]
    def has_add_permission(self, request):
        return False


    
   