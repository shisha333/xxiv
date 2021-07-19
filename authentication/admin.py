from django.conf import settings
from django.contrib import admin
from django.urls import path

from django import forms
import string
import random
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from django.core import mail
from django.core.mail import EmailMultiAlternatives

from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import UserAdmin
from authentication.models import User, Profile, Province, District, Sector, Cell, Village
from authentication.widgets import AdminFileWidget
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.shortcuts import redirect, HttpResponse

from xxivapp.models import CustomOrder

#admin.site.unregister(Group)

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name",)
    
    # def has_add_permission(self, request):
    #     return False
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "province")
    search_fields = ("name",)
    
    # def has_add_permission(self, request):
    #     return False
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    
    # def has_add_permission(self, request):
    #     return True
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False

@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    
    # def has_add_permission(self, request):
    #     return False
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False

class ProfileAdminInline(admin.StackedInline):
    model = Profile
    
    autocomplete_fields = ("district","sector", "cell")
    
    formfield_overrides = {
        models.PositiveIntegerField: {
            'widget': forms.NumberInput(
                attrs = {
                    "size": 200
                }
            )
        }
    }
    
    def save_model(self, request, obj, form, change):
        ref = string.digits
        random_number =  ''.join(random.SystemRandom().choice(ref) for _ in range(5))
        obj.pin = random_number
        super().save_model(request, obj, form, change)

@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ("first_name", "last_name")
    list_display = ("get_full_name", "email", "is_superuser", "phone", "category", 'status')
    search_fields = ("first_name", "last_name", "email", "phone")
    list_filter = []
    list_editable = ['status']
    
    inlines = [ProfileAdminInline]
    
    fieldsets = ()
    
    add_fieldsets =(
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}
        ),
    )
    
    formfield_overrides = {
        models.IntegerField: {
            'widget': forms.NumberInput(
                attrs = {
                    "size": 200
                }
            )
        }
    }
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user>/generate-confirmation-email/', self.generateConfirmationEmail, name='generate-confirmation-email'),
        ]
        return custom_urls + urls
        
    
    def get_queryset(self, request):
        if request.user.category == 'internal-territory' and not request.user.is_superuser:
            aggregators = CollectionCenter.objects.filter(territory=request.user).values_list("aggregator")
            queryset = User.objects.filter(id__in=aggregators)
            return queryset
        else:
            return super().get_queryset(request)

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "category" and not request.user.is_superuser:
            kwargs['choices'] = (("aggregator", "AGGREGATOR"),("sales-agent", "SALES AGENT"),)
        return super(UserAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups" and request.user.category != 'coordinator' and not request.user.is_superuser and 'territory' in request.user.category:
            kwargs['queryset'] = Group.objects.filter(name="aggregator")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def change_view(self, request, object_id, *args, **kwargs):
        if request.user.category == 'internal-territory':
            
            self.fieldsets = (
                (None, {'fields': ('first_name', 'last_name', 'phone', 'email', 'password', 'category')}),
                (_('Permissions'), {'fields': ('is_active', 'is_staff',
                                            'groups', )}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
        else:
            self.fieldsets = (
                (None, {'fields': ('first_name', 'last_name', 'phone', 'email', 'password', ('category', 'status'))}),
                (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                            'groups', 'user_permissions')}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
            )
        return super(UserAdmin, self).change_view(request, object_id, *args, **kwargs)
    
    def generateConfirmationEmail(self, request, user):
        user = User.objects.filter(id=user).first()
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           user=user,
        )
        
        subject = "Email Confirmartion | WarmMe"
        html_message = render_to_string('admin/authentication/confirm.html', context)

        text_content = strip_tags(html_message)
        email = "claudemani01@gmail.com"
        msg = EmailMultiAlternatives(subject, text_content, "norepley@warmme.com", [email])
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        
        return HttpResponse("message sent!")
    
        
        
        