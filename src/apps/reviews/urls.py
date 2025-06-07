from django.urls import path

from apps.reviews.views.progress import (
    HeatmapComponentView,
    PiechartComponentView,
    ProgressView,
    BarchartComponentJsonView,
)
from apps.reviews.views.review import ReviewView, SkipCardView, TurboReviewView

urlpatterns = [
    path("review/turbo/", TurboReviewView.as_view(), name="turbo"),
    path("review/<int:pk>/", ReviewView.as_view(), name="study"),
    path("review/<int:pk>/skip/", SkipCardView.as_view(), name="skip"),
    path("review/<uuid:pk>/skip-turbo/", SkipCardView.as_view(), name="skip_turbo"),
    # PROGRESS
    path("progress/", ProgressView.as_view(), name="progress"),
    path("heatmap/", HeatmapComponentView.as_view(), name="heatmap_data"),
    path("barchart/", BarchartComponentJsonView.as_view(), name="barchart_data"),
    path("piechart/", PiechartComponentView.as_view(), name="piechart_data"),
]
