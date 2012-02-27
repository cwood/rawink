from django.views.generic import CreateView, ListView, TemplateView, View
from django.conf import settings
from django.utils import translation
from django.utils import simplejson as json
from django.http import HttpResponseRedirect, HttpResponse

from .forms import ArtistForm, UserForm
import settings as _settings
from django.contrib.auth.models import Group

class Artist(CreateView):
    template_name = 'artists/artist.html'
    form_class = ArtistForm
    success_message = 'Form Sent'
    fail_message = 'Failed!'

    def get_context_data(self, **kwargs):
        context = super(Artist, self).get_context_data(**kwargs)
        context['contact_form_success'] = 'success' in self.request.GET
        context['success_message'] = self.success_message
        if self.request.POST:
            context['user_form'] = UserForm(self.request.POST)
        else:
            context['user_form'] = UserForm()    
        return context

    def get_success_url(self):
        return '%s?success' % self.request.path
    
    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        if user_form.is_valid() and form.is_valid():
            user = user_form.save()
            artist = form.save()
            user.is_staff = True
            g = Group.objects.get(name=_settings.ARTIST_GROUP)
            user.groups.add(g)
            user.save()
            
            artist.user_id = user.id
            artist.save()
                        
            response = super(Artist, self).form_valid(form)
        else:
            response = self.render_to_response(self.get_context_data(form=form))    
        return response
