# Generated by Django 4.2.1 on 2024-05-02 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SERMIS', '0002_alter_spnutricashdetails_actual_id_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spnutricashdetails',
            name='actual_ID_number',
            field=models.CharField(max_length=40),
        ),
    ]
