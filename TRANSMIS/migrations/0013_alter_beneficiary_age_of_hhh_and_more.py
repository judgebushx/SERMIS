# Generated by Django 4.2.1 on 2023-09-28 10:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TRANSMIS', '0012_alter_beneficiary_household_head_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='age_of_hhh',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(99, message='Maximum age should be 99 years or less.'), django.core.validators.MinValueValidator(0, message='Age cannot be negative.')], verbose_name='Gender of HH Head'),
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='gender_hhh',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=100, verbose_name='Gender of HH Head'),
        ),
    ]
