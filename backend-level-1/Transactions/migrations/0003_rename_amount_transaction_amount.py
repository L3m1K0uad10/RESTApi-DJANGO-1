# Generated by Django 4.0.10 on 2024-06-06 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Transactions', '0002_transaction_currency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='Amount',
            new_name='amount',
        ),
    ]
