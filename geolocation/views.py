from django.views.generic import ListView

from geolocation.models import Map


# Create your views here.
class JobsMap(ListView):
    template_name = "map.html"
    queryset = Map.objects.geojson()
