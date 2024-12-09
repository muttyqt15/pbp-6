from django import forms
from .models import Review

from api.restaurant.models import Restaurant

class ReviewForm(forms.ModelForm):
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-select searchable-select",  # Added searchable-select class
            "placeholder": "Select a restaurant"
        }),
        empty_label="Select a restaurant"
    )

    class Meta:
        model = Review
        fields = ["restaurant", "judul_ulasan", "teks_ulasan", "penilaian", "display_name"]
        widgets = {
            "judul_ulasan": forms.TextInput(attrs={
                "placeholder": "Enter review title",
                "class": "form-input"
            }),
            "teks_ulasan": forms.Textarea(attrs={
                "placeholder": "Share your experience...",
                "class": "form-textarea"
            }),
            "penilaian": forms.NumberInput(attrs={
                "min": 1,
                "max": 5,
                "class": "form-number"
            }),
        }

    def clean_penilaian(self):
        penilaian = self.cleaned_data.get("penilaian")
        if penilaian < 1 or penilaian > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return penilaian
