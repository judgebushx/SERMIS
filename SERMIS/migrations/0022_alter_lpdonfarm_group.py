# Generated by Django 4.2.1 on 2024-05-16 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SERMIS', '0021_spgfa_actual_nationality_spgfa_nationality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lpdonfarm',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lpd_onfarm_group', to='SERMIS.beneficiary'),
        ),
    ]