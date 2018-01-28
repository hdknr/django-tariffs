from django.utils.functional import cached_property
from locations_jp.models import JpAddress, City


class Tariff(object):

    @cached_property
    def instance(self):
        return self.content_type \
            and self.content_type.get_object_for_this_type(id=self.id) \
            or self


class Package(object):

    def set_charge(self, charge, prefecture=None, city=None, zipcode=None):
        if zipcode:
            qs = self.charge_set.filter(zipcode=zipcode)
            if qs.update(charge=charge, prefecture=None, city=None) > 0:
                return qs.first()
            return  self.charge_set.create(zipcode=zipcode, charge=charge)

        if city:
            qs = self.charge_set.filter(city=city)
            if qs.update(charge=charge, prefecture=None, zipcode=None) > 0:
                return qs.first()
            return  self.charge_set.create(city=city, charge=charge)

        if prefecture:
            qs = self.charge_set.filter(prefecture=prefecture)
            if qs.update(charge=charge, city=None, zipcode=None) > 0:
                return qs.first()
            return  self.charge_set.create(prefecture=prefecture, charge=charge)

    def get_charge(self, zipcode):
        if self.delegate_to:
            return self.delegate_to.get_charge(zipcode)

        charge = self.charge_set.filter(zipcode=zipcode).first()
        if not charge:
            city = City.objects.filter(jpaddress__zipcode=zipcode).first()
            charge = self.charge_set.filter(city=city).first() or\
                self.charge_set.filter(prefecture=city.prefecture).first()
        return charge and charge.charge or self.default_charge
