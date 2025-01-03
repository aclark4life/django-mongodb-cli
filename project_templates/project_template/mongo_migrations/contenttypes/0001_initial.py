# Generated by Django 5.0.10.dev20241112012728 on 2024-12-12 14:14

import django.contrib.contenttypes.models
import django_mongodb.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContentType",
            fields=[
                (
                    "id",
                    django_mongodb.fields.ObjectIdAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("app_label", models.CharField(max_length=100)),
                (
                    "model",
                    models.CharField(
                        max_length=100, verbose_name="python model class name"
                    ),
                ),
            ],
            options={
                "verbose_name": "content type",
                "verbose_name_plural": "content types",
                "db_table": "django_content_type",
                "unique_together": {("app_label", "model")},
            },
            managers=[
                ("objects", django.contrib.contenttypes.models.ContentTypeManager()),
            ],
        ),
    ]
