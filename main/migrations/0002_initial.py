# Generated by Django 4.2.7 on 2024-03-07 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(blank=True, related_name="liked_posts", to="users.profile"),
        ),
        migrations.AddField(
            model_name="post",
            name="place",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to="main.place",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="profile",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="posts", to="users.profile"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="saved",
            field=models.ManyToManyField(blank=True, related_name="saved_posts", to="users.profile"),
        ),
        migrations.AddField(
            model_name="place",
            name="region",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="districts",
                to="main.region",
            ),
        ),
        migrations.AddField(
            model_name="media",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="medias", to="main.post"
            ),
        ),
        migrations.AddField(
            model_name="media",
            name="selected_users",
            field=models.ManyToManyField(blank=True, related_name="medias", to="users.profile"),
        ),
        migrations.AddField(
            model_name="comment",
            name="likes",
            field=models.ManyToManyField(related_name="liked_comments", to="users.profile"),
        ),
        migrations.AddField(
            model_name="comment",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="users.profile"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="parent",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="children", to="main.comment"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="main.post"
            ),
        ),
    ]