from django import forms

from .models import Artwork


class ArtworkCreateForm(forms.ModelForm):

    class Meta:
        model = Artwork
        fields = ['title', 'price', 'size']