# Generated by Django 4.1.5 on 2023-03-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_rename_responsive_image_category_image2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='keywords',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
