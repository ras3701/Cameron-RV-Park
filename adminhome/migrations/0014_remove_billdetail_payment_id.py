# Generated by Django 4.0.3 on 2022-04-24 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0013_alter_billdetail_end_meter_reading_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billdetail',
            name='payment_id',
        ),
    ]
