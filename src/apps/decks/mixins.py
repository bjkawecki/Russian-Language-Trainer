from django.db.models import Q


class CourseFilterMixin:
    def get_filters(self):
        user = self.request.user
        course_filter = self.request.GET.getlist("filter")
        filters = Q(user=user)
        if course_filter:
            filters &= Q(course__name__in=course_filter)
        return filters
