# Generated by Django 3.2.20 on 2023-12-28 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_advanceduser_overtime_hours'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adress',
            options={'ordering': ['-from_date']},
        ),
        migrations.AlterModelOptions(
            name='criminal',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='salary',
            options={'ordering': ['-date']},
        ),
    ]
