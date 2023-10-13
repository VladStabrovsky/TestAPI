# Generated by Django 4.2.6 on 2023-10-11 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credits',
            name='actual_return_date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='credits',
            name='issuance_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='credits',
            name='return_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='payments',
            name='payment_date',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='users',
            name='registration_date',
            field=models.CharField(max_length=10),
        ),
    ]
