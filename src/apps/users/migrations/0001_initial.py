# Generated by Django 5.1.6 on 2025-05-31 21:23

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('bajkal_customer_id', models.CharField(editable=False, max_length=20, null=True, unique=True, verbose_name='Kundennummer')),
                ('max_new_cards', models.SmallIntegerField(default=5, verbose_name='Maximale Anzahl neue Karten')),
                ('interval_modifier', models.IntegerField(default=100, verbose_name='Intervall-Modifikator')),
                ('success_rate', models.IntegerField(default=0, verbose_name='Erfolgsrate')),
                ('show_welcome_modal', models.BooleanField(default=True, verbose_name='Willkommensnachricht anzeigen')),
                ('is_deck_name_russian', models.BooleanField(default=False, verbose_name='Stapelsprache auf Russisch')),
                ('show_examples', models.BooleanField(default=True, verbose_name='Beispiele beim Lernen anzeigen')),
                ('daily_proverb_updated', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Nutzer',
                'verbose_name_plural': 'Nutzer',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step', models.IntegerField(default=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Schritt',
                'verbose_name_plural': 'Schritte',
            },
        ),
    ]
