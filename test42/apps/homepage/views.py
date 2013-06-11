from django.views.generic import TemplateView, ListView, UpdateView
from django.core.urlresolvers import reverse_lazy
from annoying.functions import get_object_or_None
from .models import Info, LogEntry
from .forms import InfoForm


class Home(TemplateView):
    template_name = "homepage/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['info'] = get_object_or_None(Info, pk=1)
        return context


class Edit(UpdateView):
    template_name = "homepage/edit.html"
    model = Info
    form_class = InfoForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return get_object_or_None(self.model, pk=1)


class Log(ListView):
    template_name = "homepage/log.html"
    context_object_name = 'entry_list'
    queryset = LogEntry.objects.all()[0:10]
