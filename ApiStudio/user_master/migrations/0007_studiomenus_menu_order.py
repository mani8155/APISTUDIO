# Generated by Django 5.0.6 on 2024-08-17 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_master', '0006_studiomenus_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='studiomenus',
            name='menu_order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
