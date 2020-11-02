from datetime import timedelta

from constance import config

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, DeleteView, ListView
from django.views.generic.dates import timezone_today

from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm
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
        return self.model.objects.filter(user_id=self.request.user.id)


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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_initial(self):
        return {"last_date": timezone_today() + timedelta(days=config.DEFAULT_JOB_EXPIRATION)}


class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy("jobs:employer-dashboard")
    template_name = "jobsapp/delete.html"


@login_required(login_url=reverse_lazy("accounts:login"))
def filled(request, job_id=None):
    try:
        job = Job.objects.get(user_id=request.user.id, id=job_id)
        job.filled = True
        job.save()
    except IntegrityError as e:
        print(e.message)
        return HttpResponseRedirect(reverse_lazy("jobs:employer-dashboard"))
    return HttpResponseRedirect(reverse_lazy("jobs:employer-dashboard"))
