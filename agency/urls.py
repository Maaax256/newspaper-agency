from django.urls import path

from agency.views import NewspaperListView, index, RedactorListView, TopicListView

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
    )
]

app_name = "agency"