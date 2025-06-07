from django.urls import path

from apps.importer.views import (
    AdminCourseList,
    ImportCourseData,
    ImportProverbData,
    import_course_stream,
)

urlpatterns = [
    path("data-import/", AdminCourseList.as_view(), name="data_import"),
    path(
        "data-import/import-course-data/",
        ImportCourseData.as_view(),
        name="import_course",
    ),
    path(
        "data-import/import-course-data/stream/",
        import_course_stream,
        name="import_course_stream",
    ),
    path(
        "data-import/import-proverb-data/",
        ImportProverbData.as_view(),
        name="proverbs_form",
    ),
]
