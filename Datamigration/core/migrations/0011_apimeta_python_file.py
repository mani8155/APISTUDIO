# Generated by Django 5.0.4 on 2024-04-18 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_dbimport_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='apimeta',
            name='python_file',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]