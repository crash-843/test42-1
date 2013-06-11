from django import forms
from .models import Info

class InfoForm(forms.ModelForm):
    photo = forms.FileField(
                widget=forms.FileInput(attrs={'class':'special'}))
    
    class Meta:
        model = Info
