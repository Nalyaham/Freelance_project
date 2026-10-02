from django.contrib import admin
from .models import (Rental, RentalImage, RentalVideo,
                    Hostel, HostelImage, HostelVideo,
                    Airbnb, AirbnbImage, AirbnbVideo,
                    Hotel, HotelImage, HotelVideo,
                    Feedback, Lessor,)

# This line allows to stitch the child model Image model to the parent
# model so that they display on the same page.

class BaseImageInline(admin.TabularInline):
    extra = 1
    max_num = 5

class BaseVideoInline(admin.TabularInline):
    extra = 1
    max_num = 1 

# Rentals 
class RentalImageInline(BaseImageInline):
    model = RentalImage

class RentalVideoInline(BaseVideoInline):
    model = RentalVideo

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    inlines = [RentalImageInline, RentalVideoInline]
    list_display = ["name", "location", "price", "lessor", "description"]

#Hostels
class HostelImageInline(BaseImageInline):
    model = HostelImage

class HostelVideoInline(BaseVideoInline):
    model = HostelVideo

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    inlines = [HostelImageInline, HostelVideoInline]
    list_display = ["name", "location", "price", "lessor", "description"]

# Airbnbs
class AirbnbImageInline(BaseImageInline):
    model = AirbnbImage

class AirbnbVideoInline(BaseVideoInline):
    model = AirbnbVideo

@admin.register(Airbnb)
class AirbnbAdmin(admin.ModelAdmin):
    inlines = [AirbnbImageInline, AirbnbVideoInline]
    list_display = ["name", "location", "price", "lessor", "description"]

# Feedback admin page
admin.site.register(Feedback)

@admin.register(Lessor)
class LessorAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number"]
    search_fields = ["name", "phone_number"]

# Hotels
class HotelImageInline(BaseImageInline):
    model = HotelImage

class HotelVideoInline(BaseVideoInline):
    model = HotelVideo

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    inlines = [HotelImageInline, HotelVideoInline]
    search_fields = ["name", "location", "price", "lessor", "description"]
