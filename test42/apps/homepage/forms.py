from django import forms
from django.utils.safestring import mark_safe

from .models import Info


class DatePickerInput(forms.widgets.DateInput):
    def render(self, name, value, attrs=None):
        rendered = super(DatePickerInput, self).render(name, value, attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
                $(function() {
                    $('#id_%s').pikaday({
                        format: "YYYY-MM-DD"
                    });
                });
            </script>''' % name)

    class Media:
        css = {
            'all': ("homepage/css/pikaday.css",)
        }
        js = ("homepage/js/lib/moment.min.js",
              "homepage/js/lib/pikaday.js",
              "homepage/js/lib/pikaday.jquery.js",)


class InfoForm(forms.ModelForm):

    class Meta:
        model = Info
        widgets = {
            'birthday': DatePickerInput,
            'photo': forms.FileInput
        }

    class Media:
        js = ("homepage/js/lib/jquery.form.min.js",
              "homepage/js/spin.js",
              "homepage/js/edit.js",)
