# Generated by Django 4.0.3 on 2022-06-10 12:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dnccore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DialedDncNumber',
            fields=[
                ('dnc_number', models.CharField(max_length=20)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dnccore.vendor')),
            ],
        ),
    ]
