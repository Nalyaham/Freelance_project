from django.db import models

"""
YourRoom — listings/models.py

Design notes:
- BaseUnit is abstract: it just gives Rental/Airbnb/Hostel a shared set of
  fields and behaviour without creating its own DB table.
- Each unit type is its own model because their fields genuinely diverge
  (Airbnb has no room_type, Hostel has no price_max, etc). Forcing them into
  one table would mean a lot of nullable columns that don't apply to most rows.
- Each unit type has its own *Image model with a ForeignKey back to it, capped
  at 3 images via clean(). This is more code than a single generic image
  table, but it's simple to reason about and query (unit.images.all()).
"""

from django.core.exceptions import ValidationError
from django.db import models


class RoomType(models.TextChoices):
    SINGLE = "single", "Single"
    DOUBLE = "double", "Double"


class BaseUnit(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=150)

    # This makes django not to make a separate table for the base unit
    # It also orders results by location
    class Meta: 
        abstract = True
        ordering = ["name"]

    # __str__ helps to print results of code as they are in strings
    #  but not as memory references. 
    def __str__(self):
        return self.name


class Rental(BaseUnit):
    room_type = models.CharField(max_length=10, choices=RoomType.choices)
    self_contained = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Airbnb(BaseUnit):
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Hostel(BaseUnit):
    # "location" from BaseUnit can double as the general area;
    # university is the specific institution it's near, per your filters.
    university = models.CharField(max_length=150)
    room_type = models.CharField(max_length=10, choices=RoomType.choices)
    self_contained = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


# ---------------------------------------------------------------------------
# Images — one small model per unit type, each capped at 3 images.
# ---------------------------------------------------------------------------

class UnitImageBase(models.Model):
    image = models.ImageField(upload_to="units/%Y/%m/")
    is_main = models.BooleanField(
        default=False, 
        help_text="Check this box to set this image as the main display photo."
    )

    class Meta:
        abstract = True
        ordering = ["is_main"]


class RentalImage(UnitImageBase):
    unit = models.ForeignKey(Rental, related_name="images", on_delete=models.CASCADE)

   

class AirbnbImage(UnitImageBase):
    unit = models.ForeignKey(Airbnb, related_name="images", on_delete=models.CASCADE)

  

class HostelImage(UnitImageBase):
    unit = models.ForeignKey(Hostel, related_name="images", on_delete=models.CASCADE)

# Feedback Model
class Feedback(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"

   