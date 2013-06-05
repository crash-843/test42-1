from django.shortcuts import render_to_response
from django.views.generic import TemplateView, ListView
from annoying.functions import get_object_or_None
from .models import Info, LogEntry


class Home(TemplateView):
    template_name = "homepage/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['info'] = get_object_or_None(Info, pk=1)
        return context


class Log(ListView):
    template_name = "homepage/log.html"
    context_object_name = 'entry_list'
    queryset = LogEntry.objects.all()[0:10]
