from django.db import models
from django.template import Template, Context
try:
    from django.urls import reverse
except:
    from django.core.urlresolvers import reverse


def admin_change_url_name(model):
    return 'admin:{0}_{1}_change'.format(
            model._meta.app_label, model._meta.model_name, )


def admin_change_url(instance):
    return reverse(admin_change_url_name(instance), args=[instance.id])


def render(src, request=None, **kwargs):
    return Template(src).render(Context(kwargs))
