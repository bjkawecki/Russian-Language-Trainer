# Generated by Django 5.1.6 on 2025-05-31 21:23

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Titel')),
                ('message', models.TextField(max_length=2000, verbose_name='Nachricht')),
                ('is_active', models.BooleanField(default=False, verbose_name='Aktiv')),
                ('category', models.IntegerField(blank=True, choices=[(1, 'Neuigkeit'), (2, 'Erinnerung'), (3, 'Warnung')], null=True, verbose_name='Katagorie')),
                ('starting_at', models.DateTimeField(blank=True, null=True, verbose_name='Startzeit')),
            ],
            options={
                'verbose_name': 'Benachrichtigung',
                'verbose_name_plural': 'Mitteilungen',
            },
        ),
        migrations.CreateModel(
            name='UserAnnouncement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('marked_as_read', models.BooleanField(default=False, verbose_name='gelesen')),
                ('announcement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='announcements.announcement')),
            ],
            options={
                'verbose_name': 'Nutzer-Benachrichtigung',
                'verbose_name_plural': 'Nutzer-Mitteilungen',
            },
        ),
    ]
