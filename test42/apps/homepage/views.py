from django.shortcuts import render_to_response
from .models import Info
def home(request):
    try:
        info = Info.objects.get(pk=1)
    except Info.DoesNotExist:
        info = None
    return render_to_response('homepage/home.html', dict(info=info))
