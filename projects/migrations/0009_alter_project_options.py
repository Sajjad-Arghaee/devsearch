# Generated by Django 4.0 on 2022-02-09 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_review_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]