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

mechanics = {
    'Bob': {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
        'E': [],
        'F': []
    },
    'Rich': {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
        'E': [],
        'F': []
    },
    'Larry': {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
        'E': [],
        'F': []
    },
    'Simone': {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
        'E': [],
        'F': []
    },
    'Peter': {
        'A': [],
        'B': [],
        'C': [],
        'D': [],
        'E': [],
        'F': []
    }
}

repair_data = []

def get_import(request):
    print 'get_import', request
    reader = csv.reader(open('repair-data.csv'), delimiter=b' ', quotechar=b'|')
    for row in reader:
        repair_data.append(', '.join(row))
        # print(', '.join(row))
    # print repair_data[1].split(',')[1]
    # print repair_data[1].split(',')[2]

    print '1', repair_data[1].split(',')[1]
    print '2', repair_data[1].split(',')[2]
    print '3', repair_data[1].split(',')[3]
    print '4', repair_data[1].split(',')[4]
    # mechanics['Bob']['A'] = 0.0
    # print mechanics['Bob']
    return HttpResponseRedirect('/')

def parse_repair_data(repair_data):
    for i in range(1, len(repair_data)):
        data = repair_data.split(',')
        name = data[i][3]
        repair_type = data[i][4]
        time_spent = parse_time(data[1], data[2])

def parse_time(dropoff, pickup):
        date_format = "%m/%d/%Y"
        a = datetime.strptime(dropoff, date_format)
        b = datetime.strptime(pickup, date_format)
        delta = b - a
        return delta.days
