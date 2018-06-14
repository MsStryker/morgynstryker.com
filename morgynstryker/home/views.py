from django.conf import settings
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from .models import About


class IndexView(TemplateView):
    template_name = 'home/index.html'


class AboutView(DetailView):
    template_name = 'home/about.html'

    def get_object(self, queryset=None):
        try:
            obj = About.objects.get(default=True, site__id=settings.SITE_ID)
        except About.DoesNotExist:
            raise Http404('About content not found.')
        return obj
