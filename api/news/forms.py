from django.forms import ModelForm
from api.news.models import Berita
from django.utils.html import strip_tags

class BeritaEntryForm(ModelForm):
    class Meta:
        model = Berita
        fields = ["judul", "gambar", "konten"]

    def clean_judul(self):
        judul = self.cleaned_data["judul"]
        return strip_tags(judul)

    def clean_konten(self):
        konten = self.cleaned_data["konten"]
        return strip_tags(konten)
    

