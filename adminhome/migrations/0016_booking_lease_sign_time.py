# Generated by Django 4.0.3 on 2022-04-25 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminhome', '0015_billdetail_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='lease_sign_time',
            field=models.DateTimeField(null=True),
        ),
    ]
