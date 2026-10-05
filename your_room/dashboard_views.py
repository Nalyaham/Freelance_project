"""
Staff dashboard views  (your_room/dashboard_views.py)

Pages:
  /dashboard/                      overview with a card per unit type
  /dashboard/<type>/               list of units, every row editable in place
  /dashboard/<type>/add/           add a unit with its photos and video
  /dashboard/<type>/<id>/          edit a unit with its photos and video
  /dashboard/<type>/<id>/delete/   confirm and delete
"""
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    MAX_IMAGES,
    image_formset,
    unit_form,
    unit_list_formset,
    video_formset,
)
from .models import (
    Airbnb, AirbnbImage, AirbnbVideo,
    Hostel, HostelImage, HostelVideo,
    Hotel, HotelImage, HotelVideo,
    Rental, RentalImage, RentalVideo,
)

# Only active staff accounts may use the dashboard.
staff_required = user_passes_test(
    lambda u: u.is_active and u.is_staff, login_url="dash-login"
)

PAGE_SIZE = 25

# "fields" are shown both in the list rows and on the Add/Edit form.
UNIT_CONFIG = {
    "hostel": {
        "model": Hostel, "image": HostelImage, "video": HostelVideo,
        "label": "Hostel", "plural": "Hostels",
        "fields": ["name", "location", "university", "room_type",
                   "self_contained", "price", "is_booked", "lessor", "description"],
        "search": ["name", "location", "university"],
    },
    "rental": {
        "model": Rental, "image": RentalImage, "video": RentalVideo,
        "label": "Rental", "plural": "Rentals",
        "fields": ["name", "location", "room_type", "self_contained",
                   "price", "lessor", "description"],
        "search": ["name", "location"],
    },
    "airbnb": {
        "model": Airbnb, "image": AirbnbImage, "video": AirbnbVideo,
        "label": "Airbnb", "plural": "Airbnbs",
        "fields": ["name", "location", "price", "lessor", "description"],
        "search": ["name", "location"],
    },
    "hotel": {
        "model": Hotel, "image": HotelImage, "video": HotelVideo,
        "label": "Hotel", "plural": "Hotels",
        "fields": ["name", "location", "price", "lessor", "description"],
        "search": ["name", "location"],
    },
}


def get_cfg(unit_type):
    cfg = UNIT_CONFIG.get(unit_type)
    if cfg is None:
        raise Http404("Unknown unit type")
    return cfg


@staff_required
def dashboard_home(request):
    cards = [
        {"key": key, "plural": cfg["plural"], "count": cfg["model"].objects.count()}
        for key, cfg in UNIT_CONFIG.items()
    ]
    return render(request, "your_room/dashboard/home.html", {"cards": cards})


@staff_required
def unit_list(request, unit_type):
    """List of units. Every row is a form: edit any cells, then Save changes."""
    cfg = get_cfg(unit_type)
    Model = cfg["model"]

    q = request.GET.get("q", "").strip()
    units = Model.objects.order_by("-pk")          # newest first
    if q:
        condition = Q()
        for field in cfg["search"]:
            condition |= Q(**{f"{field}__icontains": q})
        units = units.filter(condition)

    # Page through the ids, then build the formset from just that page.
    paginator = Paginator(units.values_list("pk", flat=True), PAGE_SIZE)
    page_obj = paginator.get_page(request.GET.get("page"))
    page_units = (
        Model.objects.filter(pk__in=list(page_obj.object_list))
        .order_by("-pk")
        .prefetch_related("images")
    )

    FormSet = unit_list_formset(cfg)
    if request.method == "POST":
        formset = FormSet(request.POST, queryset=page_units, prefix="units")
        if formset.is_valid():
            with transaction.atomic():
                formset.save()
            changed = len(formset.changed_objects)
            deleted = len(formset.deleted_objects)
            parts = []
            if changed:
                parts.append(f"{changed} updated")
            if deleted:
                parts.append(f"{deleted} deleted")
            messages.success(request, ", ".join(parts).capitalize() + "." if parts else "No changes to save.")
            return redirect(request.get_full_path())
        messages.error(request, "Some rows have errors. Fix the highlighted cells and save again.")
    else:
        formset = FormSet(queryset=page_units, prefix="units")

    labels = [
        formset.empty_form.fields[name].label or name.replace("_", " ").capitalize()
        for name in cfg["fields"]
    ]
    return render(request, "your_room/dashboard/list.html", {
        "cfg": cfg, "unit_type": unit_type, "formset": formset,
        "labels": labels, "page_obj": page_obj, "q": q,
    })


@staff_required
def unit_edit(request, unit_type, pk=None):
    """Add (no pk) or edit (with pk) a unit together with its photos and video."""
    cfg = get_cfg(unit_type)
    obj = get_object_or_404(cfg["model"], pk=pk) if pk else None

    data = request.POST if request.method == "POST" else None
    files = request.FILES if request.method == "POST" else None
    form = unit_form(cfg)(data, files, instance=obj)
    images = image_formset(cfg)(data, files, instance=obj, prefix="images")
    videos = video_formset(cfg)(data, files, instance=obj, prefix="videos")

    if request.method == "POST":
        valid = [form.is_valid(), images.is_valid(), videos.is_valid()]  # run all three
        if all(valid):
            with transaction.atomic():
                unit = form.save()
                images.instance = unit
                videos.instance = unit
                images.save()
                videos.save()
            if obj is None:
                messages.success(
                    request,
                    f"{cfg['label']} “{unit.name}” added. You can edit its details right here in the list.",
                )
            else:
                messages.success(request, f"{cfg['label']} “{unit.name}” saved.")
            return redirect("dash-list", unit_type=unit_type)
        messages.error(request, "Please fix the errors below.")

    return render(request, "your_room/dashboard/form.html", {
        "cfg": cfg, "unit_type": unit_type, "obj": obj,
        "form": form, "images": images, "videos": videos,
        "max_images": MAX_IMAGES,
    })


@staff_required
def unit_delete(request, unit_type, pk):
    cfg = get_cfg(unit_type)
    obj = get_object_or_404(cfg["model"], pk=pk)
    if request.method == "POST":
        name = obj.name
        obj.delete()
        messages.success(request, f"{cfg['label']} “{name}” deleted.")
        return redirect("dash-list", unit_type=unit_type)
    return render(request, "your_room/dashboard/confirm_delete.html", {
        "cfg": cfg, "unit_type": unit_type, "obj": obj,
        "n_images": obj.images.count(), "n_videos": obj.videos.count(),
    })
