from django.views.generic import ListView

from geolocation.models import Map


# Create your views here.
class JobsMap(ListView):
    template_name = "map.html"

    def get_queryset(self):
        return Map.objects.geojson()
