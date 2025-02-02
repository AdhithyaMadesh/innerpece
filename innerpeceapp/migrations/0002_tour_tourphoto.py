# Generated by Django 5.0.6 on 2024-06-26 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('innerpeceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('category1', 'Category 1'), ('category2', 'Category 2'), ('category3', 'Category 3')], max_length=50)),
                ('keyword', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('day1', models.TextField()),
                ('day2', models.TextField()),
                ('day3', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('checkboxes', models.JSONField(default=list)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TourPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='tour_photos/')),
                ('tour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='innerpeceapp.tour')),
            ],
        ),
    ]
