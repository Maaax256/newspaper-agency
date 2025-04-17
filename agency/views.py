from django.shortcuts import render
from django.views import generic

from agency.models import Newspaper, Redactor, Topic


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


class RedactorListView(generic.ListView):
    model = Redactor
    template_name = "agency/redactor/redactor_list.html"


class TopicListView(generic.ListView):
    model = Topic
    template_name = "agency/topic/topic_list.html"


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    queryset = (Newspaper.objects.all()
                .select_related("topic")
                .prefetch_related("redactors"))