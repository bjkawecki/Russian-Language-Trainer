from django.contrib import admin

from apps.users.models import Step


@admin.register(Step)
class StepsAdmin(admin.ModelAdmin):
    fields = ("user", "step")
    list_display = ("user", "step")
    search_fields = ("user",)
    list_per_page = 10
