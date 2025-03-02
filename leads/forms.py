# leads/forms.py

from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'lead_type', 'price', 'budget', 'rent_budget', 'desired_property_type', 'property_type', 'rental_price', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'lead_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'rent_budget': forms.NumberInput(attrs={'class': 'form-control'}),
            'desired_property_type': forms.Select(attrs={'class': 'form-select'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'rental_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget is not None and budget <= 0:
            raise forms.ValidationError("Budget must be a positive number.")
        return budget

    def clean_rent_budget(self):
        rent_budget = self.cleaned_data.get('rent_budget')
        if rent_budget is not None and rent_budget <= 0:
            raise forms.ValidationError("Rent budget must be a positive number.")
        return rent_budget

    def clean_rental_price(self):
        rental_price = self.cleaned_data.get('rental_price')
        if rental_price is not None and rental_price <= 0:
            raise forms.ValidationError("Rental price must be a positive number.")
        return rental_price

    def clean(self):
        cleaned_data = super().clean()
        lead_type = cleaned_data.get('lead_type')

        if lead_type == 'seller':
            if not cleaned_data.get('price') or not cleaned_data.get('property_type'):
                raise forms.ValidationError("Price and Property Type are required for sellers.")
        elif lead_type == 'buyer':
            if not cleaned_data.get('budget') or not cleaned_data.get('desired_property_type'):
                raise forms.ValidationError("Budget and Desired Property Type are required for buyers.")
        elif lead_type == 'renter':
            if not cleaned_data.get('rent_budget') or not cleaned_data.get('desired_property_type'):
                raise forms.ValidationError("Rent Budget and Desired Property Type are required for renters.")
        elif lead_type == 'landlord':
            if not cleaned_data.get('rental_price') or not cleaned_data.get('property_type'):
                raise forms.ValidationError("Rental Price and Property Type are required for landlords.")

        return cleaned_data


