from django.contrib import admin

from main import models


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 0


class MediaInline(admin.TabularInline):
    model = models.Media
    extra = 0


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):

    inlines = (MediaInline, CommentInline)
    list_display = ['profile', 'type_public', 'is_show_comment', 'is_show_likes']
    list_editable = ['is_show_comment', 'is_show_likes', 'type_public']




