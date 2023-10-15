# Generated by Django 4.2.6 on 2023-10-15 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_api', '0003_alter_profile_purchase_history_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='purchase_history',
            field=models.ManyToManyField(related_name='purchase_history', to='store_api.product'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='wishlist',
            field=models.ManyToManyField(related_name='wishlist', to='store_api.product'),
        ),
    ]
