# Generated by Django 3.2 on 2021-11-20 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklists', '0003_auto_20211105_1049'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checklist',
            options={'ordering': ('priority',), 'verbose_name_plural': 'Checklist'},
        ),
        migrations.AddField(
            model_name='checklist',
            name='intent',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]