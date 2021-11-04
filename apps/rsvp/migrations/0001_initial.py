# Generated by Django 3.2 on 2021-11-04 06:56

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('weddings', '0001_initial'),
        ('guests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RSVPQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.CharField(blank=True, max_length=2000, null=True)),
                ('question_type', models.CharField(blank=True, max_length=2000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('wedding', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rsvp', to='weddings.wedding')),
            ],
            options={
                'verbose_name_plural': 'RSVP Question',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='RSVP',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer', models.CharField(blank=True, max_length=2000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('guest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rsvp', to='guests.guest')),
                ('rsvp_question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rsvp', to='rsvp.rsvpquestion')),
            ],
            options={
                'verbose_name_plural': 'RSVP',
            },
        ),
    ]
