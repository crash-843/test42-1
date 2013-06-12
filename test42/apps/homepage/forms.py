from django import forms
from .models import Info

class DatePickerInput(forms.widgets.DateInput):
    def render(self, name, value, attrs=None):
        attrs.update({"class": "date-picker"})
        return super(DatePickerInput, self).render(name, value, attrs)

class InfoForm(forms.ModelForm):
    birthday = forms.DateField(widget=DatePickerInput())
    photo = forms.FileField(widget=forms.FileInput())

    class Meta:
        model = Info
