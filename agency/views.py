from django.shortcuts import render
from django.views import generic

from agency.models import Newspaper


def index(request):
    return render(request, 'agency/index.html')


class NewspaperListView(generic.ListView):
    model = Newspaper
    template_name = "newspaper/newspaper_list.html"
    queryset = Newspaper.objects.all().select_related("topic")
