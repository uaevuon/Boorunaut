# Generated by Django 2.1.2 on 2018-11-24 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20181113_2139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'permissions': (('modify_profile', 'Can change values from all profiles.'), ('ban_user', 'Can ban users.'), ('ban_mod', 'Can ban moderators.'))},
        ),
    ]
