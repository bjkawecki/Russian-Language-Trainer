from django.urls import path

from apps.courses.views import CourseDetails, CourseList

urlpatterns = [
    path("courses/", CourseList.as_view(), name="course_list"),
    path("courses/<slug:slug>/", CourseDetails.as_view(), name="course_details"),
]
