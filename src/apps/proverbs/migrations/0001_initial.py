# Generated by Django 5.1.6 on 2025-05-31 21:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proverb',
            fields=[
                ('proverb_id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('proverb', models.TextField(blank=True, null=True, validators=[django.core.validators.RegexValidator('^[\\u0401\\u0451\\u0410-\\u044f.,:\\–\\- !?А́Е́И́О́У́Ы́Э́Ю́Я́áéи́óу́ы́э́я́ю́]*$', 'Nur kyrillische Buchstaben, Satzzeichen und Leerzeichen erlaubt.')], verbose_name='Sprichwort')),
                ('translation', models.TextField(blank=True, null=True, validators=[django.core.validators.RegexValidator("^[a-zA-Z-äöüÄÖÜß.,:?!()– ']*$", 'Nur lateinische Buchstaben, Satzzeichen und Leerzeichen erlaubt.')], verbose_name='Übersetzung')),
                ('explanation', models.TextField(blank=True, null=True, validators=[django.core.validators.RegexValidator("^[a-zA-Z-äöüÄÖÜß.,:?!()– ']*$", 'Nur lateinische Buchstaben, Satzzeichen und Leerzeichen erlaubt.')], verbose_name='Erklärung')),
                ('equivalent', models.TextField(blank=True, null=True, validators=[django.core.validators.RegexValidator("^[a-zA-Z-äöüÄÖÜß.,:?!()– ']*$", 'Nur lateinische Buchstaben, Satzzeichen und Leerzeichen erlaubt.')], verbose_name='Entsprechung')),
            ],
            options={
                'verbose_name': 'Sprichwort',
                'verbose_name_plural': 'Sprichwörter',
            },
        ),
    ]
