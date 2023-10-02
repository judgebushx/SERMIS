# Generated by Django 4.2.1 on 2023-09-29 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TRANSMIS', '0020_rename_disbursement_date_spgfa_disbursement_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='spgfa',
            name='district',
            field=models.CharField(choices=[('Koboko', 'Koboko'), ('Lamwo', 'Lamwo'), ('Isingiro', 'Isingiro'), ('Kamwenge', 'Kamwenge')], default='Koboko', max_length=100),
            preserve_default=False,
        ),
    ]
