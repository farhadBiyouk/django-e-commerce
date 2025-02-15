# Generated by Django 4.2.7 on 2016-06-03 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_product_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageProductGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('image', models.FileField(blank=True, upload_to='product_image_gallery/%Y/%m/&d')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='porduct_image', to='home.product')),
            ],
        ),
    ]
