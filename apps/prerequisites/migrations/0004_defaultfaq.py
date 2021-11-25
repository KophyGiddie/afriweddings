# Generated by Django 3.2 on 2021-11-25 17:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('prerequisites', '0003_auto_20211104_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultFAQ',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.CharField(blank=True, max_length=2000, null=True)),
                ('answer', models.CharField(blank=True, max_length=2000, null=True)),
            ],
            options={
                'verbose_name_plural': 'Default FAQ',
                'ordering': ('id',),
            },
        ),
    ]
