# Generated by Django 4.0 on 2022-02-08 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_project_options_review_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
