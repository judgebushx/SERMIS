# Generated by Django 4.2.1 on 2023-10-02 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TRANSMIS', '0031_rename_nonofffarm_hardware_component_received_lpdnonfarm_nonfarm_hardware_component_received'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='female_members',
        ),
        migrations.RemoveField(
            model_name='group',
            name='female_refugees',
        ),
        migrations.RemoveField(
            model_name='group',
            name='female_youth',
        ),
        migrations.RemoveField(
            model_name='group',
            name='male_members',
        ),
        migrations.RemoveField(
            model_name='group',
            name='male_refugees',
        ),
        migrations.RemoveField(
            model_name='group',
            name='male_youth',
        ),
        migrations.RemoveField(
            model_name='group',
            name='num_disabilities',
        ),
        migrations.RemoveField(
            model_name='group',
            name='num_refugees',
        ),
        migrations.RemoveField(
            model_name='group',
            name='num_youth',
        ),
        migrations.RemoveField(
            model_name='group',
            name='total_members',
        ),
        migrations.AddField(
            model_name='group',
            name='female_members_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='female_refugees_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='female_youth_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='male_members_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='male_refugees_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='male_youth_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='num_disabilities_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='num_refugees_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='num_youth_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='total_members_count',
            field=models.PositiveIntegerField(default='0', editable=False),
            preserve_default=False,
        ),
    ]
