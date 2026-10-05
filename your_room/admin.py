"""
Scenario B: Django's own admin, with every list editable in place
(your_room/admin.py).

How it works
  * "Add hostel" (top right of the list) opens the usual add page.
  * After saving, you land on the list, where each row's fields are inputs.
    Change what you need, then press "Save" at the bottom of the table.
  * Click "Edit" at the start of a row for the full page with photos and video.
"""
from django.contrib import admin
from django.contrib.admin.widgets import AdminTextareaWidget
from django.db import models
from django.utils.html import format_html

from .models import (
    Airbnb, AirbnbImage, AirbnbVideo,
    Feedback,
    Hostel, HostelImage, HostelVideo,
    Hotel, HotelImage, HotelVideo,
    Lessor,
    Rental, RentalImage, RentalVideo,
)


# ---------------------------------------------------------------------------
# Photo and video rows on each unit's full edit page
# ---------------------------------------------------------------------------
class BaseImageInline(admin.TabularInline):
    extra = 3
    max_num = 5          # photos per unit


class BaseVideoInline(admin.TabularInline):
    extra = 1
    max_num = 1          # one video per unit


class RentalImageInline(BaseImageInline):
    model = RentalImage

class RentalVideoInline(BaseVideoInline):
    model = RentalVideo

class HostelImageInline(BaseImageInline):
    model = HostelImage

class HostelVideoInline(BaseVideoInline):
    model = HostelVideo

class AirbnbImageInline(BaseImageInline):
    model = AirbnbImage

class AirbnbVideoInline(BaseVideoInline):
    model = AirbnbVideo

class HotelImageInline(BaseImageInline):
    model = HotelImage

class HotelVideoInline(BaseVideoInline):
    model = HotelVideo


# ---------------------------------------------------------------------------
# Shared behaviour for all four unit types
# ---------------------------------------------------------------------------
class UnitAdmin(admin.ModelAdmin):
    list_per_page = 25
    save_on_top = True
    list_display_links = ["edit_link"]     # lets every real field be editable in the list

    # Keeps the description box compact in the list rows.
    # (This also applies on the full edit page. Raise "rows" if you want it taller there.)
    formfield_overrides = {
        models.TextField: {"widget": AdminTextareaWidget(attrs={"rows": 3, "cols": 36})},
    }

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("images")

    @admin.display(description="Open")
    def edit_link(self, obj):
        return "Edit"

    @admin.display(description="Photo")
    def thumb(self, obj):
        images = list(obj.images.all())
        if not images:
            return "-"
        return format_html(
            '<img src="{}" style="width:64px;height:48px;object-fit:cover;border-radius:6px">',
            images[0].image.url,
        )


@admin.register(Hostel)
class HostelAdmin(UnitAdmin):
    list_display = ["edit_link", "thumb", "name", "location", "university", "room_type",
                    "self_contained", "price", "is_booked", "lessor", "description"]
    list_editable = ["name", "location", "university", "room_type",
                     "self_contained", "price", "is_booked", "lessor", "description"]
    list_filter = ["is_booked", "room_type", "self_contained", "university"]
    search_fields = ["name", "location", "university", "description"]
    inlines = [HostelImageInline, HostelVideoInline]
    actions = ["mark_booked", "mark_available"]

    @admin.action(description="Mark selected hostels as booked")
    def mark_booked(self, request, queryset):
        n = queryset.update(is_booked=True)
        self.message_user(request, f"{n} hostel(s) marked as booked.")

    @admin.action(description="Mark selected hostels as available")
    def mark_available(self, request, queryset):
        n = queryset.update(is_booked=False)
        self.message_user(request, f"{n} hostel(s) marked as available.")


@admin.register(Rental)
class RentalAdmin(UnitAdmin):
    list_display = ["edit_link", "thumb", "name", "location", "room_type",
                    "self_contained", "price", "lessor", "description"]
    list_editable = ["name", "location", "room_type", "self_contained",
                     "price", "lessor", "description"]
    list_filter = ["room_type", "self_contained", "location"]
    search_fields = ["name", "location", "description"]
    inlines = [RentalImageInline, RentalVideoInline]


@admin.register(Airbnb)
class AirbnbAdmin(UnitAdmin):
    list_display = ["edit_link", "thumb", "name", "location", "price", "lessor", "description"]
    list_editable = ["name", "location", "price", "lessor", "description"]
    list_filter = ["location"]
    search_fields = ["name", "location", "description"]
    inlines = [AirbnbImageInline, AirbnbVideoInline]


@admin.register(Hotel)
class HotelAdmin(UnitAdmin):
    list_display = ["edit_link", "thumb", "name", "location", "price", "lessor", "description"]
    list_editable = ["name", "location", "price", "lessor", "description"]
    list_filter = ["location"]
    search_fields = ["name", "location", "description"]
    inlines = [HotelImageInline, HotelVideoInline]


# ---------------------------------------------------------------------------
# Other models
# ---------------------------------------------------------------------------
admin.site.register(Feedback)


@admin.register(Lessor)
class LessorAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number"]
    search_fields = ["name", "phone_number"]
