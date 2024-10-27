from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["judul_ulasan", "teks_ulasan", "penilaian", "display_name"]
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