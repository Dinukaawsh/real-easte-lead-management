# Generated by Django 5.1.5 on 2025-02-26 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='desired_property_type',
            field=models.CharField(blank=True, choices=[('apartment', 'Apartment'), ('house', 'House'), ('condo', 'Condo')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='property_type',
            field=models.CharField(blank=True, choices=[('apartment', 'Apartment'), ('house', 'House'), ('condo', 'Condo')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='rent_budget',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='rental_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
