# Generated by Django 5.0.4 on 2024-04-10 05:28

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiMeta',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uid', models.CharField(max_length=255, unique=True)),
                ('table_details', models.TextField()),
                ('api_name', models.CharField(max_length=255, unique=True)),
                ('psk_uid', models.CharField(default=uuid.uuid4, max_length=255)),
                ('api_type', models.CharField(max_length=255)),
                ('api_method', models.CharField(max_length=255)),
                ('api_source', models.CharField(max_length=255)),
                ('db_connection', models.IntegerField()),
                ('db_connection_name', models.CharField(max_length=255)),
                ('python_code', models.TextField()),
                ('python_file', models.BinaryField()),
                ('code_name', models.TextField()),
                ('document_url', models.CharField(max_length=255)),
                ('api_property', models.TextField(default='API_DEFAULT_PROPERTY')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'api_meta',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('table_name', models.CharField(max_length=255, unique=True)),
                ('table_name_public', models.CharField(max_length=255)),
                ('uid', models.CharField(max_length=255, unique=True)),
                ('psk_uid', models.CharField(default=uuid.uuid4, max_length=255)),
                ('published', models.BooleanField(default=False)),
                ('version', models.IntegerField(default=0)),
                ('relations', models.CharField(max_length=255)),
                ('db_connection', models.IntegerField()),
                ('db_connection_name', models.CharField(max_length=255)),
                ('readonly', models.BooleanField(default=False)),
                ('document_url', models.CharField(max_length=255)),
                ('has_media', models.BooleanField(default=False)),
                ('has_posts', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'api_models',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('field_name', models.CharField(max_length=255)),
                ('field_name_public', models.CharField(max_length=255)),
                ('psk_uid', models.CharField(default=uuid.uuid4, max_length=255)),
                ('field_data_type', models.CharField(max_length=255)),
                ('related_to', models.CharField(max_length=255)),
                ('published', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('field_property', models.TextField(default='{}')),
                ('field_rule', models.TextField()),
                ('field_select', models.TextField()),
                ('table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='core.table')),
            ],
            options={
                'db_table': 'api_fields',
            },
        ),
    ]