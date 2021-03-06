# Generated by Django 4.0 on 2022-05-02 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItineraryAppManagement', '0003_itinerariesimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Itineraries')),
            ],
        ),
        migrations.AddField(
            model_name='itineraries',
            name='banner',
            field=models.ImageField(default='', upload_to='Itineraries'),
        ),
    ]
