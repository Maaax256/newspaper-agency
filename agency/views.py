from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import NewspaperForm, RedactorForm
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


class RedactorListView(generic.ListView):
    model = Redactor
    template_name = "agency/redactor/redactor_list.html"


class TopicListView(generic.ListView):
    model = Topic
    template_name = "agency/topic/topic_list.html"


class MyNewspapersListView(generic.ListView):
    model = Newspaper
    template_name = "agency/newspaper/newspaper_list.html"

    def get_queryset(self):
        user = self.request.user
        return user.newspapers.all()


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    queryset = (Newspaper.objects.all()
                .prefetch_related("topics")
                .prefetch_related("redactors"))
    template_name = "agency/newspaper/newspaper_detail.html"


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = (Redactor.objects.all()
                .prefetch_related("newspapers"))
    template_name = "agency/redactor/redactor_detail.html"


class TopicDetailView(generic.DetailView):
    model = Topic
    queryset = Topic.objects.all().prefetch_related("newspapers")
    template_name = "agency/topic/topic_detail.html"


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")
    template_name = "agency/newspaper/newspaper_form.html"


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")
    template_name = "agency/newspaper/newspaper_form.html"


class ProfileUpdateView(generic.UpdateView):
    model = Redactor
    form_class = RedactorForm
    success_url = reverse_lazy("agency:home")
    template_name = "agency/redactor/redactor_form.html"
