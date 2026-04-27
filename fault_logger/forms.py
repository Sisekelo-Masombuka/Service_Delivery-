from django import forms

from .models import FaultReport


class FaultReportForm(forms.ModelForm):
    def __init__(self, *args, translated_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        if translated_choices is not None:
            self.fields["issue_type"].choices = translated_choices

    class Meta:
        model = FaultReport
        fields = (
            "issue_type",
            "description",
            "image",
            "is_hazard",
            "latitude",
            "longitude",
        )
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 6,
                    "class": "input-control",
                    "aria-describedby": "desc-hint",
                }
            ),
            "issue_type": forms.Select(attrs={"class": "input-control"}),
            # Hide technical coordinates; set via mini-map + GPS in the UI
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "is_hazard": forms.CheckboxInput(
                attrs={"class": "hazard-checkbox", "role": "switch"}
            ),
            "image": forms.ClearableFileInput(
                attrs={"class": "file-input", "accept": "image/*"}
            ),
        }
