# Generated by Django 5.0.6 on 2024-08-12 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_master', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiomenus',
            name='menu_ui_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]