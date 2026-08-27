
from your_room.models import Rental, Hostel, Airbnb
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
import uuid
from nylonpay import create_nylon_pay
from nylonpay import SdkException

UNIT_MODELS = { 'rental' : Rental, 
               'hostel' : Hostel, 
               'airbnb' : Airbnb}


def index(request):
    rental_location = Rental.objects.values_list("location", flat=True).distinct()
    airbnb_location = Airbnb.objects.values_list("location", flat=True).distinct()
    university = Hostel.objects.values_list("university", flat=True).distinct()

    context = { "rental_locations" :rental_location,
               "airbnb_locations" : airbnb_location,
                "universities" : university 
                }

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
    units = Airbnb.objects.prefetch_related("images")

    location = request.GET.get("location")
    name = request.GET.get("name")

    if location: 
        units = units.filter(location__icontains = location)
    if name: 
        units = units.filter(name__icontains = name)

    context = { "locations" : Airbnb.objects.values_list("location", flat=True).distinct(), 
               "names" : Airbnb.objects.values_list("name", flat=True).distinct(),
               "units": units}
    
    return render(request, "your_room/airbnb.html", context)

# your_room/views.py

from your_room.models import Rental, Hostel, Airbnb

def search(request):
    q = request.GET.get("q", "").strip()
    words = q.split()

    rentals = hostels = airbnbs = []

    if words:
        rental_filter = Q()
        for word in words:
            rental_filter &= (
                Q(name__icontains=word)
                | Q(location__icontains=word)
            )
        rentals = Rental.objects.filter(rental_filter).prefetch_related("images")

        hostel_filter = Q()
        for word in words:
            hostel_filter &= (
                Q(name__icontains=word)
                | Q(university__icontains=word)
                | Q(location__icontains=word)
            )
        hostels = Hostel.objects.filter(hostel_filter).prefetch_related("images")

        airbnb_filter = Q()
        for word in words:
            airbnb_filter &= (
                Q(name__icontains=word)
                | Q(location__icontains=word)
                | Q(description__icontains=word)
            )
        airbnbs = Airbnb.objects.filter(airbnb_filter).prefetch_related("images")

    results = (
        [{"unit": u, "type": "rental"} for u in rentals]
        + [{"unit": u, "type": "hostel"} for u in hostels]
        + [{"unit": u, "type": "airbnb"} for u in airbnbs]
    )
    return render(request, "your_room/search.html", {"q": q, "results": results})

nylonpay = create_nylon_pay(
    api_key=settings.NYLONPAY_API_KEY,
    api_secret=settings.NYLONPAY_API_SECRET
)

def book_now(request, unit_type, pk):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

# From here the view collects information of the model being bought and the number making the purchase. 
    model = UNIT_MODELS.get(unit_type)
    unit = get_object_or_404(model, pk=pk) # This line gets the unit
    name = request.POST.get("name")
    phone = request.POST.get("phone_number")

    try:
        payment = nylonpay.collect_payment(
            amount= int(unit.price),
            currency="UGX",
            customer={"name": name, "phone_number": phone},
            description= f"Booking: {unit.name}",
            reference=str(uuid.uuid4())
        )
    except SdkException as e:
        print(f"Category: {e.category}")
        print(f"Retryable: {e.retryable}")
        print(f"Message: {e}")

    result = payment.wait()

    print("RESULT:", result)
    print("PAYMENT STATUS:", payment.status)
    print("PAYMENT REFERENCE:", payment.reference)

    if result is not None:
        return JsonResponse({"status": "success", "transaction_id": result.id})
    else:
        return JsonResponse({"status": "failed"})