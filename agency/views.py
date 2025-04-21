from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from agency.forms import (NewspaperForm,
                          RedactorCreationForm,
                          RedactorUpdateForm)
from agency.models import Newspaper, Redactor, Topic


@login_required
def index(request):
    context = {}
    top_exp_redactors = get_user_model().objects.order_by(
        "-years_of_experience"
    )[:10]
    context["top_exp_redactors"] = top_exp_redactors
    return render(
        request,
        "agency/home.html",
        context=context
    )


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.all().order_by("title")
    template_name = "agency/newspaper/newspaper_list.html"


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = get_user_model()
    queryset = get_user_model().objects.all().order_by("last_name")
    template_name = "agency/redactor/redactor_list.html"


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    queryset = Topic.objects.all().order_by("name")
    template_name = "agency/topic/topic_list.html"


class MyNewspapersListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    template_name = "agency/newspaper/newspaper_list.html"

    def get_queryset(self):
        user = self.request.user
        return user.newspapers.all().order_by("title")


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    queryset = (Newspaper.objects.all()
                .prefetch_related("topics")
                .prefetch_related("redactors"))
    template_name = "agency/newspaper/newspaper_detail.html"


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = get_user_model()
    queryset = (Redactor.objects.all()
                .prefetch_related("newspapers"))
    template_name = "agency/redactor/redactor_detail.html"


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic
    queryset = Topic.objects.all().prefetch_related("newspapers")
    template_name = "agency/topic/topic_detail.html"


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")
    template_name = "agency/newspaper/newspaper_form.html"


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("agency:newspaper-list")
    template_name = "agency/newspaper/newspaper_form.html"


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = RedactorUpdateForm
    success_url = reverse_lazy("agency:home")
    template_name = "agency/redactor/redactor_form.html"


class RegistrationView(LoginRequiredMixin, generic.CreateView):
    model = get_user_model()
    form_class = RedactorCreationForm
    success_url = reverse_lazy("agency:home")
    template_name = "agency/redactor/redactor_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("agency:newspaper-list")
    template_name = "agency/newspaper/newspaper_confirm_delete.html"