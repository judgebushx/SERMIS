# Generated by Django 4.2.1 on 2023-10-02 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TRANSMIS', '0033_alter_group_other_partner_assistance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='disablity_of_hhh',
            field=models.CharField(choices=[('Able bodied', 'Able bodied'), ('Living with a disability', 'Living with a disability')], max_length=100),
        ),
    ]
