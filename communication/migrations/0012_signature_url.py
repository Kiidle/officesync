# Generated by Django 3.2.20 on 2023-11-06 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0011_alter_signature_zip'),
    ]

    operations = [
        migrations.AddField(
            model_name='signature',
            name='url',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Webseite'),
        ),
    ]