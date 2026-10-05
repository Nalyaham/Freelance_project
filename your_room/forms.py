"""
Forms for the staff dashboard  (your_room/forms.py)

One set of factory functions builds the forms for all four unit types, so a
change here (for example, the photo limit) applies to Hostels, Rentals,
Airbnbs and Hotels at once.
"""
from django import forms
from django.core.exceptions import ValidationError
from django.forms import (
    BaseInlineFormSet,
    inlineformset_factory,
    modelform_factory,
    modelformset_factory,
)

MAX_IMAGES = 5   # photos allowed per unit. Change here to allow more or fewer.
MAX_VIDEOS = 1   # videos allowed per unit.


class ImageFormSet(BaseInlineFormSet):
    """Photo rows for one unit. Allows at most one 'main' photo."""

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        mains = sum(
            1
            for f in self.forms
            if f.cleaned_data
            and not f.cleaned_data.get("DELETE")
            and f.cleaned_data.get("is_main")
        )
        if mains > 1:
            raise ValidationError("Choose only one main photo.")


def unit_form(cfg):
    """Full form used on the Add and Edit pages."""
    return modelform_factory(
        cfg["model"],
        fields=cfg["fields"],
        widgets={"description": forms.Textarea(attrs={"rows": 4})},
    )


def unit_list_formset(cfg):
    """One editable row per unit, used on the list page."""
    return modelformset_factory(
        cfg["model"],
        fields=cfg["fields"],
        extra=0,
        can_delete=True,
        widgets={"description": forms.Textarea(attrs={"rows": 2})},
    )


def image_formset(cfg):
    return inlineformset_factory(
        cfg["model"],
        cfg["image"],
        formset=ImageFormSet,
        fields=["image", "is_main"],
        extra=3,
        max_num=MAX_IMAGES,
        validate_max=True,
        can_delete=True,
    )


def video_formset(cfg):
    return inlineformset_factory(
        cfg["model"],
        cfg["video"],
        fields=["video"],
        extra=1,
        max_num=MAX_VIDEOS,
        validate_max=True,
        can_delete=True,
    )
