from django.db import models
import uuid
from django.core.exceptions import ValidationError

class Lead(models.Model):
    LEAD_TYPES = [
        ('seller', 'Seller'),
        ('buyer', 'Buyer'),
        ('renter', 'Renter'),
        ('landlord', 'Landlord'),
    ]

    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condo'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    lead_type = models.CharField(max_length=10, choices=LEAD_TYPES)
    location = models.CharField(max_length=255)

    # Seller-specific fields
    price = models.IntegerField(null=True, blank=True)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, null=True, blank=True)

    # Buyer-specific fields
    budget = models.IntegerField(null=True, blank=True)
    desired_property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, null=True, blank=True)

    # Renter-specific fields
    rent_budget = models.IntegerField(null=True, blank=True)

    # Landlord-specific fields
    rental_price = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.lead_type}"

    def clean(self):
        """Ensure required fields are filled based on lead type."""
        if self.lead_type == 'seller' and not self.property_type:
            raise ValidationError("Sellers must specify a property type.")
        if self.lead_type == 'buyer' and not self.desired_property_type:
            raise ValidationError("Buyers must specify a desired property type.")

    def clean_price(self):
        # Custom validation for price (example)
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

    def clean_budget(self):
        # Custom validation for budget (example)
        budget = self.cleaned_data.get('budget')
        if budget and budget <= 0:
            raise forms.ValidationError('Budget must be greater than zero.')
        return budget
    def save(self, *args, **kwargs):
        """Ensure only relevant fields are populated based on lead type."""
        self.clean()

        if self.lead_type == 'buyer':
            self.price = None
            self.property_type = None
            self.rent_budget = None
            self.rental_price = None
        
        elif self.lead_type == 'seller':
            self.budget = None
            self.rent_budget = None
            self.desired_property_type = None
            self.rental_price = None
        
        elif self.lead_type == 'renter':
            self.price = None
            self.property_type = None
            self.budget = None
            self.rental_price = None
        
        elif self.lead_type == 'landlord':
            self.budget = None
            self.rent_budget = None
            self.desired_property_type = None

        super().save(*args, **kwargs)
