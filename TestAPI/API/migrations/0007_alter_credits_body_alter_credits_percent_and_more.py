# Generated by Django 4.2.6 on 2023-10-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0006_alter_credits_actual_return_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credits',
            name='body',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='credits',
            name='percent',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='payments',
            name='sum',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='plans',
            name='sum',
            field=models.FloatField(),
        ),
    ]
