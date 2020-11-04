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
    CATEGORY_SOFTWARE_DEVELOPER = "software-developer"
    CATEGORY_DATA_ANALYST = "data-analyst"
    CATEGORY_MOBILE_DEVELOPER_JUNIOR_ANDROID = "mobile-android-junior-developer"
    CATEGORY_MOBILE_DEVELOPER_MEDIOR_ANDROID = "mobile-android-medior-developer"
    CATEGORY_MOBILE_DEVELOPER_SENIOR_ANDROID = "mobile-android-senior-developer"
    CATEGORY_MOBILE_DEVELOPER_JUNIOR_IOS = "mobile-ios-junior-developer"
    CATEGORY_MOBILE_DEVELOPER_MEDIOR_IOS = "mobile-ios-medior-developer"
    CATEGORY_MOBILE_DEVELOPER_SENIOR_IOS = "mobile-ios-senior-developer"
    CATEGORY_FRONTEND_WEB_DEVELOPER_JUNIOR = "frontend-junior-developer"
    CATEGORY_FRONTEND_WEB_DEVELOPER_MEDIOR = "frontend-medior-developer"
    CATEGORY_FRONTEND_WEB_DEVELOPER_SENIOR = "frontend-senior-developer"
    CATEGORY_BACKEND_WEB_DEVELOPER_JUNIOR = "backend-junior-developer"
    CATEGORY_BACKEND_WEB_DEVELOPER_MEDIOR = "backend-medior-developer"
    CATEGORY_BACKEND_WEB_DEVELOPER_SENIOR = "backend-senior-developer"
    CATEGORY_FULLSTACK_WEB_DEVELOPER_JUNIOR = "fullstack-junior-developer"
    CATEGORY_FULLSTACK_WEB_DEVELOPER_MEDIOR = "fullstack-medior-developer"
    CATEGORY_FULLSTACK_WEB_DEVELOPER_SENIOR = "fullstack-senior-developer"
    CATEGORY_PRODUCT_OWNER = "product-owner"
    CATEGORY_PROJECT_MANAGER = "project-manager"
    CATEGORY_LEAD_SOFTWARE_ENGINEER = "lead-software-engineer"
    CATEGORY_SECURITY_SPECIALIST = "security-specialist"
    CATEGORY_SYSADMIN = "sysadmin"
    CATEGORY_DEVOPS = "devops"
    CATEGORY_DATABASE_ADMINISTRATOR = "database-administrator"

    CATEGORIES = (
        (CATEGORY_WEB_DESIGN, _("Web design")),
        (CATEGORY_GRAPHIC_DESIGN, _("Graphic design")),
        (CATEGORY_SOFTWARE_DEVELOPER, _("Sofware developer")),
        (CATEGORY_DATA_ANALYST, _("Data analyst")),
        (CATEGORY_MOBILE_DEVELOPER_JUNIOR_ANDROID, _("Junior Mobile developer Android")),
        (CATEGORY_MOBILE_DEVELOPER_MEDIOR_ANDROID, _("Medior Mobile developer Android")),
        (CATEGORY_MOBILE_DEVELOPER_SENIOR_ANDROID, _("Senior Mobile developer Android")),
        (CATEGORY_MOBILE_DEVELOPER_JUNIOR_IOS, _("Junior Mobile developer iOS")),
        (CATEGORY_MOBILE_DEVELOPER_MEDIOR_IOS, _("Medior Mobile developer iOS")),
        (CATEGORY_MOBILE_DEVELOPER_SENIOR_IOS, _("Senior Mobile developer iOS")),
        (CATEGORY_FRONTEND_WEB_DEVELOPER_JUNIOR, _("Junior Frontend developer")),
        (CATEGORY_FRONTEND_WEB_DEVELOPER_MEDIOR, _("Medior Frontend developer")),
        (CATEGORY_FRONTEND_WEB_DEVELOPER_SENIOR, _("Senior Frontend developer")),
        (CATEGORY_BACKEND_WEB_DEVELOPER_JUNIOR, _("Junior Backend developer")),
        (CATEGORY_BACKEND_WEB_DEVELOPER_MEDIOR, _("Medior Backend developer")),
        (CATEGORY_BACKEND_WEB_DEVELOPER_SENIOR, _("Senior Backend developer")),
        (CATEGORY_FULLSTACK_WEB_DEVELOPER_JUNIOR, _("Junior Fullstack developer")),
        (CATEGORY_FULLSTACK_WEB_DEVELOPER_MEDIOR, _("Medior Fullstack developer")),
        (CATEGORY_FULLSTACK_WEB_DEVELOPER_SENIOR, _("Senior Fullstack developer")),
        (CATEGORY_PRODUCT_OWNER, _("Product Owner")),
        (CATEGORY_PROJECT_MANAGER, _("Project Manager")),
        (CATEGORY_LEAD_SOFTWARE_ENGINEER, _("Lead software engineer")),
        (CATEGORY_SECURITY_SPECIALIST, _("Security specialist")),
        (CATEGORY_SYSADMIN, _("Sysadmin")),
        (CATEGORY_DEVOPS, _("Devops")),
        (CATEGORY_DATABASE_ADMINISTRATOR, _("Database administrator")),
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
