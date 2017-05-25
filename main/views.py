# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Service
from .forms import ServiceForm

# Create your views here.
def index(request):
    print 'request', request
    services = Service.objects.all()
    form = ServiceForm()
    return render(request, 'index.html',
                    {'services': services, 'form': form})

def post_service(request):
    form = ServiceForm(request.POST)
    if form.is_valid():
        service = Service(dropoff = form.cleaned_data['dropoff'],
                          pickup = form.cleaned_data['pickup'],
                          mechanic = form.cleaned_data['mechanic'],
                          repair_type = form.cleaned_data['repair_type'])
        service.save()
    return HttpResponseRedirect('/')

national_averages = {
    'A': 1.0,
    'B': 1.0,
    'C': 3.0,
    'D': 2.0,
    'E': 3.0,
    'F': 2.5
}

mechanics = {}
repair_data = []

def get_import(request):
    reader = csv.reader(open('repair-data.csv'), delimiter=b' ', quotechar=b'|')
    for row in reader:
        repair_data.append(', '.join(row))
    parse_repair_data(repair_data)
    return HttpResponseRedirect('/')

def parse_repair_data(repair_data):
    for i in range(1, len(repair_data)):
        data = repair_data[i].split(',')
        name = data[3]
        repair_type = data[4]
        time_spent = parse_time(data[1], data[2])
        if name not in mechanics.keys():
            mechanics[name] = {
                'A': [],
                'B': [],
                'C': [],
                'D': [],
                'E': [],
                'F': []
            }
            mechanics[name][repair_type] = [time_spent]
        else:
            mechanics[name][repair_type].append(time_spent)
    print mechanics

def parse_time(dropoff, pickup):
    if dropoff == '' or dropoff == 'Dropoff' or pickup == '' or pickup == 'Pickup':
        return None
    date_format = "%m/%d/%Y"
    a = datetime.strptime(dropoff, date_format)
    b = datetime.strptime(pickup, date_format)
    delta = b - a
    return delta.days
