from django.contrib import admin

from apps.courses.models import Course
from apps.decks.models import Deck
from apps.users.models import User


class InlineDecks(admin.StackedInline):
    model = Deck
    extra = 0


class InlineUsers(admin.TabularInline):
    model = User.course_set.through
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ("name", "json_file", "slug")
    list_per_page = 10
    readonly_fields = ("id",)
    list_display = ("name", "json_file")
    inlines = [InlineUsers, InlineDecks]
