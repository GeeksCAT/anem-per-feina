from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import FormView

# from ..documents import JobDocument
from ..models import Job
from ..forms import ContactForm
from ..models import Job


class HomeView(ListView):
    model = Job
    template_name = "home.html"
    context_object_name = "jobs"

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trendings"] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


class SearchView(ListView):
    model = Job
    template_name = "jobs/search.html"
    context_object_name = "jobs"

    def get_queryset(self):
        # q = JobDocument.search().query("match", title=self.request.GET['position']).to_queryset()
        # print(q)
        # return q
        return self.model.objects.filter(
            location__contains=self.request.GET["location"],
            title__contains=self.request.GET["position"],
        )


class JobListView(ListView):
    model = Job
    template_name = "jobs/jobs.html"
    context_object_name = "jobs"
    paginate_by = 5


class JobDetailsView(DetailView):
    model = Job
    template_name = "jobs/details.html"
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
    success_url = "/contact-us"
    success_message = _("Mensage sent successfully")

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
