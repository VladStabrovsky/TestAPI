# Generated by Django 4.2.6 on 2023-10-11 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_alter_credits_body_alter_credits_percent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credits',
            name='actual_return_date',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
