# Generated by Django 5.1.6 on 2025-05-31 21:25

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('words', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('due_date', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('initial', 'neu'), ('in_progress', 'aktiv'), ('mastered', 'gemeistert'), ('review', 'üben')], default='initial', verbose_name='Lernstatus')),
                ('ease', models.IntegerField(default=170, validators=[django.core.validators.MaxValueValidator(250), django.core.validators.MinValueValidator(130)])),
                ('interval', models.IntegerField(default=0, verbose_name='Lernschritt')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Nutzer')),
                ('word', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='words.word', verbose_name='Karte')),
            ],
            options={
                'verbose_name': 'Karte',
                'verbose_name_plural': 'Karten',
                'ordering': ['word__lemma'],
            },
        ),
    ]
