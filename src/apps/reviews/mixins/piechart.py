from apps.courses.models import Course


class PiechartMixin:
    def get_course_choices(self, user):
        return Course.objects.filter(user=user).values("id", "name")
