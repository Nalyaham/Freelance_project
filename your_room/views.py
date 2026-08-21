
from your_room.models import Rental, Hostel, Airbnb
from django.shortcuts import render, get_object_or_404

UNIT_MODELS = { 'rental' : Rental, 
               'hostel' : Hostel, 
               'airbnb' : Airbnb}


def index(request):
    location = Rental.objects.values_list("location", flat=True).distinct()
    location = Airbnb.objects.values_list("location", flat=True).distinct()
    location = Hostel.objects.values_list("university", flat=True).distinct()

    context = { "locations" : location }

    return render(request, "your_room/index.html", context)

def rental(request):
    units = Rental.objects.prefetch_related("images")

    location = request.GET.get("location")
    room_type = request.GET.get("room_type")
    self_contained = request.GET.get("self_contained")

    if location:
        units = units.filter(location__icontains=location)
    if room_type:
        units = units.filter(room_type=room_type)
    if self_contained in ("true", "false"):
        units = units.filter(self_contained=(self_contained == "true"))

    context = {
        "units": units,
        # feeds the location dropdown with whatever locations actually exist
        "locations": Rental.objects.values_list("location", flat=True).distinct(),
    }
    return render(request, "your_room/rentals.html", context)


# Unit_type is a parameter added to the link sending the request
# If the link has a unit type equal to the model in the dictionary, detail will only display that list
def unit_detail(request,unit_type, pk): 
    model = UNIT_MODELS.get(unit_type)
    unit = get_object_or_404(model.objects.prefetch_related("images"), pk=pk)
    return render(request, "your_room/detail.html", {"unit": unit, "unit_type": unit_type})

def hostel(request):
    units = Hostel.objects.prefetch_related("images")

    university = request.GET.get("university")
    room_type = request.GET.get("room_type")
    self_contained = request.GET.get("self_contained")

    if university:
        units = units.filter(university__icontains=university)
    if room_type:
        units = units.filter(room_type=room_type)
    if self_contained in ("true", "false"):
        units = units.filter(self_contained=(self_contained == "true"))

    context = {
        "units": units,
        # feeds the location dropdown with whatever locations actually exist
        "universities": Hostel.objects.values_list("university", flat=True).distinct(),
    }
    return render(request, "your_room/hostels.html", context)

def airbnb(request):
    return render(request, "your_room/airbnb.html")

def search(request):
    return render(request, "your_room/search.html")