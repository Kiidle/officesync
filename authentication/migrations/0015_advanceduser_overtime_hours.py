# Generated by Django 3.2.20 on 2023-12-28 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_alter_advanceduser_biographie'),
    ]

    operations = [
        migrations.AddField(
            model_name='advanceduser',
            name='overtime_hours',
            field=models.FloatField(blank=True, null=True),
        ),
    ]