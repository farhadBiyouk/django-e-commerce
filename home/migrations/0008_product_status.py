# Generated by Django 4.2.7 on 2016-06-01 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_color_size_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, choices=[('None', 'none'), ('Size', 'size'), ('Color', 'Color')], max_length=10, null=True),
        ),
    ]
