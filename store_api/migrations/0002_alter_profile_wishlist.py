# Generated by Django 4.2.6 on 2023-10-30 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='wishlist',
            field=models.ManyToManyField(null=True, related_name='wishlist', to='store_api.product'),
        ),
    ]
