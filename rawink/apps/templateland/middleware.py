from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.template.base import TemplateDoesNotExist
import re


class TemplateFallbackMiddleware(object):
    """Falls back to showing a template, if it exists."""

    def process_response(self, request, response):
        if isinstance(response, HttpResponseNotFound):
            template = re.sub(r'^/+|/+$', '', request.path)
            for t in [template, '%s.html' % template, '%s.json' % template]:
                try:
                    response = render(request, t)
                    break
                except TemplateDoesNotExist:
                    pass
        return response
