from django.views.generic import ListView

from geolocation.models import Address


# Create your views here.
class JobsMap(ListView):
    template_name = "map.html"
    queryset = Address.objects.geojson()
