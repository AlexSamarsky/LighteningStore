# Generated by Django 4.1.5 on 2023-03-28 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='collection',
            field=models.CharField(default=0, max_length=150, verbose_name='kolleksiyon'),
            preserve_default=False,
        ),
    ]