from class_based_auth_views.views import LoginView
from rawink.apps.artists.models import ArtistWorkPhoto
import urlparse

from django.shortcuts import get_object_or_404

class LoginView(LoginView):
    template_name = 'main/user.html'
    
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update({self.redirect_field_name: self.request.GET.get('next')})
        if self.request.GET.get('next'):
            o  = urlparse.urlparse(self.request.GET.get('next'))
            qs = urlparse.parse_qs(o.query)
            try:
                product = qs.get('product')[0]
                if product:
                    product = get_object_or_404(ArtistWorkPhoto, slug=product)
                    context.update({'product': product})
            except:
                pass
        return context