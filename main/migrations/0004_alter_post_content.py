# Generated by Django 4.2.7 on 2024-03-08 16:20

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0003_post_watchers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]