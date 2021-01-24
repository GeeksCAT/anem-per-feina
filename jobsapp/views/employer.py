from datetime import timedelta

from constance import config

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.dates import timezone_today

from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm, EditJobForm
from jobsapp.models import Job


class DashboardView(ListView):
    model = Job
    template_name = "jobsapp/employer/dashboard.html"
    context_object_name = "jobs"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.job_set.all().order_by("-created_at")


class JobUpdateView(UpdateView):
    template_name = "jobsapp/update.html"
    form_class = EditJobForm
    extra_context = {"title": _("Edit Job")}
    success_url = reverse_lazy("jobs:employer-dashboard")

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        job = get_object_or_404(Job, user=self.request.user, pk=self.kwargs["pk"])
        return job


from geolocation.forms import CreateAddressForm


class JobCreateView(CreateView):
    template_name = "jobsapp/create.html"
    form_class = CreateJobForm
    extra_context = {"title": _("Post New Job")}
    success_url = reverse_lazy("jobs:employer-dashboard")

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy("accounts:login")
        return super().dispatch(self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["AddressForm"] = CreateAddressForm(self.request.POST)
            print(data["AddressForm"])
        else:
            data["AddressForm"] = CreateAddressForm()
            # breakpoint()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        # save job
        form.instance.user = self.request.user
        address = context["AddressForm"]
        if address.is_valid():
            job_address = address.save()
            job = form.save()

            job.geo_location = job_address
            job.save()

        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        last_date = timezone_today() + timedelta(days=config.DEFAULT_JOB_EXPIRATION)
        return {"last_date": last_date}


class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy("jobs:employer-dashboard")
    template_name = "jobsapp/delete.html"

    @method_decorator(login_required(login_url=reverse_lazy("accounts:login")))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_object(self, queryset=None):
        job = get_object_or_404(Job, user=self.request.user, pk=self.kwargs["pk"])
        return job


@login_required(login_url=reverse_lazy("accounts:login"))
def filled(request, job_id):
    job = get_object_or_404(Job, user=request.user, pk=job_id)
    job.filled = not job.filled
    job.save()
    return HttpResponseRedirect(reverse_lazy("jobs:employer-dashboard"))
