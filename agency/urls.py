from django.urls import path

from agency.views import (NewspaperListView,
                          index,
                          RedactorListView,
                          TopicListView,
                          NewspaperDetailView)

urlpatterns = [
    path("", index, name="home"),
    path(
        "newspapers/",
        NewspaperListView.as_view(),
        name="newspaper-list"
    ),
    path(
        "redactors/",
        RedactorListView.as_view(),
        name="redactor-list"
    ),
    path(
        "topics/",
        TopicListView.as_view(),
        name="topic-list"
    ),

    path(
        "newspapers/<int:pk>/",
        NewspaperDetailView.as_view(),
        name="newspaper-detail"
    )
]

app_name = "agency"