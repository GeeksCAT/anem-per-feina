import pytest

from django.contrib.gis.geos import Point
from django.contrib.gis.geos.point import Point

from geolocation.geo_utils import CoordinatesNotFound, GeoCoder


def test_convert_full_address_to_coordinates():
    address = "Plaça del Vi 27, Girona, Girona, Catalonia, 17001, Spain"
    street, city, county, state, postalcode, country = address.split(",")

    geodata = GeoCoder()
    geodata.get_coordinates(
        street=street, city=city, county=county, state=state, postalcode=postalcode, country=country
    )

    assert all([hasattr(geodata, "lat"), hasattr(geodata, "lon")])
    assert geodata.lat == 41.9828528
    assert geodata.lon == 2.8244397
    assert isinstance(geodata.geo_point, Point)


def test_fail_get_coordinates_from_address():
    city = "Gironaa"
    country = "Catalunya"

    with pytest.raises(CoordinatesNotFound) as e:
        geodata = GeoCoder()
        geodata.get_coordinates(city=city, country=country)


@pytest.mark.django_db
def test_add_new_address(address_factory):
    address = address_factory(county="Girona")
    assert address.county == "Girona"
    assert address.city == "Girona"


@pytest.mark.django_db
def test_set_coordinates_to_address(address_factory):
    address = "Plaça del Vi, 27, Girona, Girona, Catalonia, 17001, Spain"
    street, number, city, county, state, postalcode, country = address.split(",")
    new_address = address_factory(
        street=street,
        number=number,
        city=city,
        county=county,
        state=state,
        postalcode=postalcode,
        country=country,
    )

    assert all((new_address.lat is None, new_address.lat is None))
    lat = 41.9828528
    lon = 2.8244397
    new_address.set_coordinates(lat, lon)
    assert all((new_address.lat == lat, new_address.lon == lon))
