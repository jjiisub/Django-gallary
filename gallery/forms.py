from django import forms

from .models import Artwork, Exhibition


class ArtworkCreateForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'price', 'size']


class ExhibitionCreateForm(forms.ModelForm):
    class Meta:
        model = Exhibition
        fields = ['title', 'start_date', 'end_date', 'artworks']
    
    def __init__(self, user, *args, **kwargs):
        super(ExhibitionCreateForm, self).__init__(*args, **kwargs)
        self.fields['artworks'].queryset = Artwork.objects.filter(artist=user.artist)
    
    artworks = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class':'form-check-input me-1'}
        )
    )
