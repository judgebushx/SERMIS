# Generated by Django 4.2.1 on 2024-05-06 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SERMIS', '0006_alter_spnutricashdetails_id_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutricashbeneficiary',
            name='exit_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
