from django.contrib import admin
from tariffs import models, utils
from . import forms

class Mixin(object):

    def admin_url(self, obj):
        return utils.render('''<a href="{{u}}">{{i}}</a>''',
            u=utils.admin_change_url(obj), i=obj)


class ChargeInline(admin.TabularInline):
    model = models.Charge
    fields = ['charge', 'prefecture', 'city', 'zipcode']
    extra = 0
    raw_id_fields =['city']


class PackageInline(admin.TabularInline, Mixin):
    model = models.Package
    readonly_fields = ['admin_url']
    extra = 0
    form = forms.PackageForm
    formset = forms.PackageInlineFormSet

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(PackageInline, self).get_formset(request, obj, **kwargs)
        formset.request = request
        return formset
