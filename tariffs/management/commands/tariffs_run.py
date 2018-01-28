from django.utils.datastructures import MultiValueDict as _D
from django.http import QueryDict

from django.utils import translation
from pyexcel_xlsx import get_data as excel_get_data
import djclick as click
from tariffs import models, defs, filters
from locations_jp.models import JpAddress, City, Prefecture

from logging import getLogger
import zipfile
import requests
import io
import json
import csv
import unicodedata
log = getLogger()

translation.activate('ja')


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.argument('charge')
@click.argument('package_id', nargs=-1)
@click.option('--zipcode', '-z', multiple=True)
@click.option('--pref', '-p', multiple=True)
@click.option('--city', '-c', multiple=True)
@click.pass_context
def set_charge(ctx, charge, package_id, zipcode, pref, city):
    '''Set Charge for Package '''
    if not package_id:
        click.echo("package_id is required")
        return

    for package in models.Package.objects.filter(id__in=package_id):
        if zipcode:
            for code in zipcode:
                package.set_charge(charge, zipcode=code)
            return

        cities = city and City.objects.filter(jiscode__in=city)
        if cities:
            for city in cities:
                package.set_charge(charge, city=city)
            return

        prefs =  pref and Prefecture.objects.filter(name__in=pref)
        if prefs:
            for p in prefs:
                package.set_charge(charge, prefecture=p)
            return



@main.command()
@click.option('--charge', '-c', multiple=True)
@click.option('--package', '-p', multiple=True)
@click.option('--zipcode', '-z', multiple=True)
@click.option('--pref')
@click.option('--city')
@click.pass_context
def list_charge(ctx, charge, package, zipcode, pref, city):
    '''List Charges for Tariff '''

    query = {}
    if charge:
        query['charge__in'] = charge
    if package:
        query['package__slug__in'] = package
    if zipcode:
        query['zipcode__in'] = zipcode
    if pref:
        query['prefecture__name'] = pref
    if city:
        query['city__name__contains'] = city

    for obj in models.Charge.objects.filter(**query):
        click.echo("{} {} {}".format(
            str(obj.destination), str(obj.package), obj.charge))


@main.command()
@click.argument('zipcode')
@click.option('--package', '-p', multiple=True)
@click.pass_context
def get_charge(ctx, zipcode, package):
    packages = package and models.Package.objects.filter(id__=package) or\
        models.Package.objects.all()

    click.echo("Addresses for Zipcode:".format(zipcode))
    for addr in JpAddress.objects.filter(zipcode=zipcode):
        click.echo(addr)

    click.echo()
    click.echo("Charge:")
    for package in packages:
        click.echo("{} {}".format(str(package), package.get_charge(zipcode)))
