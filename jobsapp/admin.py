from django.contrib import admin  # noqa

# Register your models here.
from jobsapp.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "salary",
        "location",
        "type",
        "category",
        "company_name",
        "last_date",
        "created_at",
        "filled",
        "user",
        "remote",
    ]
    list_filter = ["salary", "last_date", "created_at", "user", "remote"]
    date_hierarchy = "created_at"
