# Generated by Django 3.2 on 2021-11-04 06:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('prerequisites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=2000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Country',
                'ordering': ('name',),
            },
        ),
    ]
