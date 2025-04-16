from django.shortcuts import render
from django.views import generic

from agency.models import Newspaper, Redactor


def index(request):
    context = {}
    top_exp_redactors = Redactor.objects.order_by("-years_of_experience")[:10]
    context["top_exp_redactors"] = top_exp_redactors
    return render(
        request,
        "agency/home.html",
        context=context
    )


class NewspaperListView(generic.ListView):
    model = Newspaper
    template_name = "agency/newspaper/newspaper_list.html"
    queryset = Newspaper.objects.all().select_related("topic")
