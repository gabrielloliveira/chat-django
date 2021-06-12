from django.contrib import admin

from apps.core.models import HelpDesk, Client, Message

admin.site.register(Client)


@admin.register(HelpDesk)
class HelpDeskAdmin(admin.ModelAdmin):
    list_display = ("uuid", "client", "created_at")
    search_fields = ["client"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("uuid", "help_desk", "type", "created_at")
    list_filter = ["type"]

