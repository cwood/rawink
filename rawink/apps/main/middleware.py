
class SetGroupMiddleware(object):
    def process_request(self, request):
        if not request.user.is_anonymous():
            if 'usergroup' not in request.session:
                groups = request.user.groups.all()
                if groups:
                    request.session['usergroup'] = str(groups[0].name)