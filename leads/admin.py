from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from .models import Lead

class LeadAdminForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'

    class Media:
        js = ('admin/js/lead_dynamic_fields.js',)  # Link custom JavaScript

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    form = LeadAdminForm
    list_display = ('name', 'lead_type', 'location', 'price', 'budget', 'rent_budget', 'rental_price', 'created_at')
    list_filter = ('lead_type', 'location')
    search_fields = ('name', 'location')

    def get_fields(self, request, obj=None):
        """Define form fields based on lead type"""
        fields = ['name', 'lead_type', 'location']
        if obj:
            if obj.lead_type == 'seller':
                fields += ['price', 'property_type']
            elif obj.lead_type == 'buyer':
                fields += ['budget']
            elif obj.lead_type == 'renter':
                fields += ['rent_budget', 'desired_property_type']
            elif obj.lead_type == 'landlord':
                fields += ['rental_price', 'property_type']
        return fields

    def get_form(self, request, obj=None, **kwargs):
        """Modify form to include a dynamic script"""
        form = super().get_form(request, obj, **kwargs)
        return form
