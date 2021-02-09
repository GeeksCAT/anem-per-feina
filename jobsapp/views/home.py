from typing import Any, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormView

from ..forms import ContactForm
from ..models import Job


class HomeView(ListView):
    model = Job
    template_name = "home.html"
    context_object_name = "jobs"

    def get_queryset(self):
        return self.model.objects.unfilled()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trendings"] = self.model.objects.unfilled(created_at__month=timezone.now().month)[
            :3
        ]
        return context


class SearchView(ListView):
    model = Job
    template_name = "jobsapp/search.html"
    context_object_name = "jobs"

    def get_queryset(self):
        queryset = self.model.objects.all()

        location = self.request.GET.get("location")
        if location:
            queryset = queryset.filter(location__icontains=location)

        position = self.request.GET.get("position")
        if position:
            queryset = queryset.filter(title__icontains=position)

        return queryset


class JobListView(ListView):
    model = Job
    template_name = "jobsapp/jobs.html"
    context_object_name = "jobs"
    paginate_by = 5


class JobDetailsView(DetailView):
    model = Job
    template_name = "jobsapp/details.html"
    context_object_name = "job"
    pk_url_kwarg = "id"

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404(_("Job doesn't exists"))
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # raise error
            raise Http404(_("Job doesn't exists"))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ContactView(FormView):
    template_name = "contact_us.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_email()
        messages.info(self.request, _("Mensage sent successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, _("Mensage not sent"))
        return super().form_invalid(form)
