# Generated by Django 4.0.10 on 2024-06-08 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reviews', '0002_alter_review_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]