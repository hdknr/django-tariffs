from django.contrib import admin
from ordered_model.admin import OrderedTabularInline, OrderedModelAdmin
from tariffs import models, utils
from . import inlines, forms


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'zipcode', 'pref_name', 'city_name', 'town_name']
    fields = [
        'jiscode', 'zipcode', 'pref_name', 'city_name', 'town_name',
        'all_packages',
    ]
    search_fields = ['pref_name', 'city_name', 'town_name',
                     'pref_kana', 'city_kana', 'town_kana', ]
    list_filter = ['pref_name']

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields] + ['all_packages']

    def all_packages(self, obj):
        packages = [{'package':p, 'charge': p.get_charge(obj.zipcode)}
                    for p in models.Package.objects.all()]
        return utils.render('''
        <table>
        {% for p in ps %}
         <tr><td><a href="{% url 'admin:tariffs_package_change' p.package.id %}">{{ p.package}}</a></td>
         <td>{{ p.charge }}</td></tr>
        {% endfor %}
        </table>
        ''', ps=packages)
    all_packages.short_description = "Packages"
    all_packages.allow_tags = True


@admin.register(models.Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    readonly_fields = ['content_type', 'admin_url']
    inlines = [inlines.PackageInline]

    def admin_url(self, obj):
        obj = obj.instance
        return utils.render('''<a href="{{u}}">{{i}}</a>''',
            u=utils.admin_change_url(obj), i=obj)

    def _create_formsets(self, request, obj, change):
        setattr(request, '_current_tarrif', obj)
        return super(TariffAdmin, self)._create_formsets(
            request, obj, change)


@admin.register(models.Package)
class PackageAdmin(OrderedModelAdmin):
    form = forms.PackageForm
    raw_id_fields = ['tariff']
    list_filter = ['tariff', 'can_mix']
    list_display = [
        'id', 'tariff', 'slug', 'name', 'delegate_to',
        'default_charge', 'can_mix', 'free_limit', 'seq', 'move_up_down_links']
    readonly_fields = ['seq', 'move_up_down_links',]
    inlines = [inlines.ChargeInline]


@admin.register(models.Charge)
class ChargeAdmin(OrderedModelAdmin):
    list_display = [
        'id', 'package', 'charge', 'prefecture', 'city', 'zipcode',
        'seq', 'move_up_down_links']
    readonly_fields = ['seq', 'move_up_down_links',]
    raw_id_fields = ['package', 'prefecture', 'city', ]


@admin.register(models.Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = [f.name for f in models.Slot._meta.fields]
