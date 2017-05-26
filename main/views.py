# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
from datetime import datetime
from collections import defaultdict

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

repair_data = []
def get_import(request):
    reader = csv.reader(open('repair-data.csv'), delimiter=b' ', quotechar=b'|')
    for row in reader:
        repair_data.append(', '.join(row))
    parse_repair_data(repair_data)
    return HttpResponseRedirect('/')

mechanics = defaultdict(lambda: defaultdict(list))
def parse_repair_data(repair_data):
    for i in range(1, len(repair_data)):
        data = repair_data[i].split(',')
        name = data[3]
        repair_type = data[4]
        time_spent = parse_time(data[1], data[2])
        mechanics[name][repair_type].append(time_spent)
    for mechanic in mechanics:
        get_average_repair_time(mechanic, mechanics[mechanic])

def parse_time(dropoff, pickup):
    if (not dropoff or dropoff == 'Dropoff' or
        not pickup or pickup == 'Pickup'):
        return None
    date_format = "%m/%d/%Y"
    start = datetime.strptime(dropoff, date_format)
    end = datetime.strptime(pickup, date_format)
    delta = end - start
    return delta.days

def get_average_repair_time(mechanic, repairs):
    for repair in repairs:
        filtered = [item
          for item
          in repairs.get(repair, [])
          if item is not None and int(item) > 0]
        average = sum(filtered) / len(filtered) if filtered else 0
        print repair, average
