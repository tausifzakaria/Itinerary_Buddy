# Generated by Django 3.2.9 on 2022-05-15 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_account_country_account_mobile_account_nationality'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(default='profile_pic', null=True, upload_to=''),
        ),
    ]
