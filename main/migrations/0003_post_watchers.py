# Generated by Django 4.2.7 on 2024-03-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_remove_storywatchers_count"),
        ("main", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="watchers",
            field=models.ManyToManyField(blank=True, related_name="watching_posts", to="users.profile"),
        ),
    ]
