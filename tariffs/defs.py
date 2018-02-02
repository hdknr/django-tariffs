from django.db import models
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModelBase


class OrderedModel(OrderedModelBase):
    seq = models.PositiveIntegerField(editable=False, db_index=True)
    order_field_name = 'seq'

    class Meta:
        abstract = True


class Tariff(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True


class Package(OrderedModel):
    slug = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    default_charge = models.DecimalField(
        _('Default Charge'), max_digits=6, decimal_places=0, default=0)

    class Meta:
        abstract = True


class Charge(OrderedModel):
    zipcode = models.CharField(
        max_length=10, db_index=True,
        null=True, blank=True, default=None)
    charge = models.DecimalField(
        _('Distination Charge'), max_digits=6, decimal_places=0, default=0)

    class Meta:
        abstract = True


class Slot(models.Model):
    '''Time Slot'''
    label = models.CharField(max_length=50)
    time_from = models.TimeField(null=True, blank=True, default=None)
    time_to = models.TimeField(null=True, blank=True, default=None)

    class Meta:
        abstract = True
