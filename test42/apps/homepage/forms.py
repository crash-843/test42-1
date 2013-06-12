from django import forms
from ajax_upload.widgets import AjaxClearableFileInput
from .models import Info


class DatePickerInput(forms.widgets.DateInput):
    def render(self, name, value, attrs=None):
        attrs.update({"class": "date-picker"})
        return super(DatePickerInput, self).render(name, value, attrs)


class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        widgets = {
            'birthday': DatePickerInput,
            'photo': AjaxClearableFileInput
        }
