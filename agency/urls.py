from django.urls import path

from agency.views import NewspaperListView, index

urlpatterns = [
    path("", index, name="index"),
    path(
        "newspapers/",
        NewspaperListView.as_view(),
        name="newspaper-list"
    )
]

app_name = "agency"