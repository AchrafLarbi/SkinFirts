# Generated by Django 4.2.4 on 2024-07-27 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='experience_years',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]