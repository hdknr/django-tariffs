from django import forms
from tariffs import models


class PackageForm(forms.ModelForm):
    class Meta:
        model = models.Package
        exclude = []

    def __init__(self, *args, **kwargs):
        super(PackageForm, self).__init__(*args, **kwargs)
        tariff = ('instance' in kwargs) and getattr(
            kwargs['instance'], 'tariff', None) or None

        if tariff:
            self.patch_tariff(self, tariff)            

    @classmethod
    def patch_tariff(cls, form, tariff):
        qs = form.fields['mixes'].queryset.filter(tariff=tariff)
        form.fields['mixes'].queryset = qs

        qs = form.fields['delegate_to'].queryset.filter(tariff=tariff)
        form.fields['delegate_to'].queryset = qs
        return form


class PackageInlineFormSet(forms.models.BaseInlineFormSet):
    model = models.Package

    def __init__(self, *args, **kwargs):
        self.current_tariff = hasattr(self, 'request') \
            and getattr(self.request, '_current_tarrif', None) or None
        super(PackageInlineFormSet, self).__init__(*args, **kwargs)

    @property
    def empty_form(self):
        form = super(PackageInlineFormSet, self).empty_form
        return self.current_tariff and \
            form.patch_tariff(form, self.current_tariff) or form