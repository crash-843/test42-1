import json
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, UpdateView
from django.core.urlresolvers import reverse_lazy
from annoying.functions import get_object_or_None
from .models import Info, LogEntry
from .forms import InfoForm


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            context = self.ajax_invalid_context_data(**form.errors)
            return self.render_to_json_response(context, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            context = self.ajax_valid_context_data(pk=self.object.pk)
            return self.render_to_json_response(context)
        else:
            return response

    def ajax_valid_context_data(self, **kwargs):
        return kwargs

    def ajax_invalid_context_data(self, **kwargs):
        return kwargs


class Home(TemplateView):
    template_name = "homepage/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['info'] = get_object_or_None(Info, pk=1)
        return context


class Edit(AjaxableResponseMixin, UpdateView):
    template_name = "homepage/edit.html"
    model = Info
    form_class = InfoForm
    success_url = reverse_lazy('home')
    thumbnail_options = dict(size=(300, 400), crop=True)

    def get_object(self, queryset=None):
        return get_object_or_None(self.model, pk=1)

    def ajax_valid_context_data(self, **kwargs):
        context = super(Edit, self).ajax_valid_context_data(**kwargs)
        thumbnail = self.object.photo.get_thumbnail(self.thumbnail_options)
        context['photo'] = thumbnail.url if thumbnail else None
        return context


class Log(ListView):
    template_name = "homepage/log.html"
    context_object_name = 'entry_list'
    queryset = LogEntry.objects.all()[0:10]
