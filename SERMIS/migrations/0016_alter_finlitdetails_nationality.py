# Generated by Django 4.2.1 on 2024-05-15 07:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SERMIS', '0015_finlitdetails_actual_nationality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finlitdetails',
            name='nationality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='finlit_nationality', to='SERMIS.finlitbeneficiary'),
        ),
    ]