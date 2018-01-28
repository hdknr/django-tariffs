from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from locations_jp.models import Prefecture, City, JpAddress
from . import defs, methods

class Address(JpAddress):

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')
        proxy = True


class Tariff(defs.Tariff, methods.Tariff):
    content_type = models.ForeignKey(
        ContentType, null=True, default=None, blank=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Tariff')
        verbose_name_plural = _('Tariffs')

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(self)
        if content_type.model != 'tariff' and content_type.app_label != 'tariffs':
            self.content_type = content_type
        super(Tariff, self).save(*args, **kwargs)


class Package(defs.Package, methods.Package):
     tariff = models.ForeignKey(
         Tariff, on_delete=models.CASCADE)

     delegate_to = models.ForeignKey(
         'self', on_delete=models.SET_NULL,
         related_name='delegated_by',
         null=True, blank=True, default=None)

     mixes = models.ManyToManyField(
         'self', blank=True, symmetrical=False)

     order_class_path = 'tariffs.models.Package'
     order_with_respect_to = ('tariff', )

     class Meta:
         verbose_name = _('Package')
         verbose_name_plural = _('Packages')
         ordering = ['tariff', 'seq', ]

     def __str__(self):
         return "{} {}".format(str(self.tariff), self.name)


class Charge(defs.Charge):
     package = models.ForeignKey(Package, on_delete=models.CASCADE)
     prefecture = models.ForeignKey(
        Prefecture, on_delete=models.SET_NULL,
        null=True, blank=True, default=None)
     city = models.ForeignKey(
        City, on_delete=models.SET_NULL,
        null=True, blank=True, default=None)

     order_class_path = 'tariffs.models.Charge'
     order_with_respect_to = ('package', )

     class Meta:
         verbose_name = _('Charge')
         verbose_name_plural = _('Charges')
         ordering = ['package', 'seq', ]
