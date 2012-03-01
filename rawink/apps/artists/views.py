from django.views.generic import CreateView, ListView, DetailView, TemplateView, View
from django.conf import settings
from django.utils import translation
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse

import settings as _settings
from django.contrib.auth.models import Group

from .models import Artist

class ArtistIndex(ListView):
    model = Artist


class ArtistDetail(DetailView):
    model = Artist
