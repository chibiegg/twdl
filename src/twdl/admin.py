# encoding=utf-8

from django.contrib import admin
from twdl.models import User, Status

class UserAdmin(admin.ModelAdmin):
    list_display = ["id_str", "screen_name", "name", "created_at"]


class StatusAdmin(admin.ModelAdmin):
    list_display = ["id_str", "author", "text", "created_at"]
    search_fields = ["text"]

admin.site.register(User, UserAdmin)
admin.site.register(Status, StatusAdmin)

