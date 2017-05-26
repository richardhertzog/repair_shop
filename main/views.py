# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
from datetime import datetime
from collections import defaultdict

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Service
from .forms import ServiceForm

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


def get_import(request):
    with open('repair-data.csv') as csvfile:
      reader = csv.reader(csvfile)
      header = True
      for row in reader:
        if header:
          print "skipping header", row
          header = False
          continue
        print "processing row", row
        parse_repair_data(row)
    for name, timings in mechanics.iteritems():
      averages = get_average_repair_time(timings)
      report(name, averages)

    return HttpResponseRedirect('/')

mechanics = defaultdict(lambda: defaultdict(list))
def parse_repair_data(repair_data):
    name = repair_data[3]
    repair_type = repair_data[4]
    print repair_data[1], repair_data[2]
    time_spent = parse_time(repair_data[1], repair_data[2])
    mechanics[name][repair_type].append(time_spent)
    print "parsed", repair_data, "into: ", name, repair_type, time_spent

def parse_time(dropoff, pickup):
    if dropoff and pickup:
      date_format = "%m/%d/%Y"
      start = datetime.strptime(dropoff, date_format)
      end = datetime.strptime(pickup, date_format)
      delta = end - start
      return delta.days
    else:
      return None

def get_average_repair_time(timings):
    retval = dict()
    for repair, times in timings.iteritems():
      filtered = [item
        for item
        in times
        if item is not None and int(item) > 0]
      average = float(sum(filtered)) / len(filtered) if filtered else 0.0
      retval[repair] = average
    return retval

NATIONAL_AVERAGES = {
  'A': 1.0,
  'B': 1.0,
  'C': 3.0,
  'D': 2.0,
  'E': 3.0,
  'F': 2.5
}
def report(name, averages):
  for repair, time in averages.iteritems():
    if not repair in NATIONAL_AVERAGES:
      continue

    expected = NATIONAL_AVERAGES[repair]
    if time < expected:
      print name, "was faster at", repair
    elif time > expected:
      print name, "was slower at", repair
    else:
      print name, "finished", repair, "on time"
