from django.contrib import admin
from .models import Rental, RentalImage, Hostel, HostelImage, Airbnb, AirbnbImage, Feedback, Lessor

# This line allows to stitch the child model Image model to the parent
# model so that they display on the same page. 
class RentalImageInline(admin.TabularInline):
    model = RentalImage
    extra = 1 # Pre-displays 3 empty image upload rows
    max_num = 3  # Matches your model restriction

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    inlines = [RentalImageInline]
    list_display = ["name", "location", "price", "lessor"]

class HostelImageInline(admin.TabularInline):
    model = HostelImage
    extra = 1  # Pre-displays 3 empty image upload rows
    max_num = 3  # Matches your model restriction

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    inlines = [HostelImageInline]
    list_display = ["name", "location", "price", "lessor"]

class AirbnbImageInline(admin.TabularInline):
    model = AirbnbImage
    extra = 1 # Pre-displays 3 empty image upload rows
    max_num = 3  # Matches your model restriction

@admin.register(Airbnb)
class AirbnbAdmin(admin.ModelAdmin):
    inlines = [AirbnbImageInline]
    list_display = ["name", "location", "price", "lessor"]

# Feedback admin page
admin.site.register(Feedback)

@admin.register(Lessor)
class LessorAdmin(admin.ModelAdmin):
    list_display = ["name", "phone_number"]
    search_fields = ["name", "phone_number"]
