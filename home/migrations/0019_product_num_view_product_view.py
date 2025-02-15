# Generated by Django 4.2.7 on 2016-08-16 01:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0018_variant_update_chart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_view',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='view',
            field=models.ManyToManyField(blank=True, related_name='product_view', to=settings.AUTH_USER_MODEL),
        ),
    ]
