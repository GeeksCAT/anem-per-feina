# DJANGO Imports
from inclusive_django_range_fields import InclusiveIntegerRangeField

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _

# APP Imports
from accounts.models import User
from notifications.decorators import event_dispatcher
from notifications.events import EVENT_NEW_JOB

# Global Imports
JOB_INDEXES = ("location", "category", "type", "title")

# Job remote types


@event_dispatcher(EVENT_NEW_JOB)
class Job(models.Model):
    JOB_TYPE_FULL_TIME = "1"
    JOB_TYPE_PART_TIME = "2"
    JOB_TYPE_INTERNSHIP = "3"
    JOB_TYPES = (
        (JOB_TYPE_FULL_TIME, _("Full time")),
        (JOB_TYPE_PART_TIME, _("Part time")),
        (JOB_TYPE_INTERNSHIP, _("Internship")),
    )
    NO_REMOTE = "1"
    REMOTE = "2"
    PARTIAL_REMOTE = "3"
    REMOTE_CHOICES = (
        (NO_REMOTE, _("No remote")),
        (REMOTE, _("Full remote")),
        (PARTIAL_REMOTE, _("Partial remote")),
    )

    CATEGORY_WEB_DESIGN = "web-design"
    CATEGORY_GRAPHIC_DESIGN = "graphic-design"
    CATEGORY_WEB_DEVELOPMENT = "web-development"

    CATEGORIES = (
        (CATEGORY_WEB_DESIGN, _("Web design")),
        (CATEGORY_GRAPHIC_DESIGN, _("Graphic design")),
        (CATEGORY_WEB_DEVELOPMENT, _("Web development")),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("User who creates this job."),
    )
    title = models.CharField(
        max_length=300, verbose_name=_("Title"), help_text=_("Short job title.")
    )
    description = models.TextField(
        verbose_name=_("Description"), help_text=_("Long job description.")
    )
    location = models.CharField(
        max_length=150, verbose_name=_("Location"), help_text=_("Location for this job position.")
    )
    type = models.CharField(
        choices=JOB_TYPES, max_length=10, verbose_name=_("Type"), help_text=_("Job type.")
    )
    category = models.CharField(
        max_length=100,
        verbose_name=_("Category"),
        help_text=_("Category clasification."),
        choices=CATEGORIES,
    )
    last_date = models.DateField(verbose_name=_("Last date"), help_text=_("Last date."))
    company_name = models.CharField(
        max_length=100, verbose_name=_("Company"), help_text=_("Job's Company name.")
    )
    company_description = models.CharField(
        max_length=300,
        verbose_name=_("Company description"),
        help_text=_("Company description, activity,..."),
    )
    website = models.CharField(
        max_length=100, default="", verbose_name=_("Website"), help_text=_("Company Website URL.")
    )
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name=_("Created"), help_text=_("Job creation date and time.")
    )
    filled = models.BooleanField(
        default=False, verbose_name=_("Filled"), help_text=_("Job position is filled.")
    )
    salary = models.PositiveIntegerField(
        verbose_name=_("Salary"),
        help_text=_("Minimum and maximum annual salary for this job."),
        default=None,
        blank=True,
        null=True,
    )
    remote = models.CharField(
        verbose_name=_("Remote"),
        null=True,
        choices=REMOTE_CHOICES,
        max_length=20,
        help_text=_("Is this job position remote?."),
    )
    apply_url = models.URLField(
        max_length=200,
        verbose_name=_("Apply URL"),
        help_text=_("Users will apply on your website."),
        default="",
    )

    class Meta:
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")
        indexes = [models.Index(fields=(field,)) for field in JOB_INDEXES]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("jobs:jobs-detail", kwargs={"id": self.id})
