# Generated by Django 4.2.1 on 2024-05-13 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SERMIS', '0009_alter_spsagedetails_id_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spsagedetails',
            old_name='actual_ID_number',
            new_name='actual_candidate_individual_id',
        ),
        migrations.RenameField(
            model_name='spsagedetails',
            old_name='ID_number',
            new_name='candidate_individual_id',
        ),
    ]
