# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Service
from .forms import ServiceForm

# Create your views here.
def index(request):
    print 'request', request.GET
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
    print 'get_import', request
    spamReader = csv.reader(open('repair-data.csv'), delimiter=b' ', quotechar=b'|')
    for row in spamReader:
        print(', '.join(row))
    return HttpResponseRedirect('/')

# def export_csv(request):
#     print 'export beginning'
#     if(request.POST.post('export')):
#         print "EXPORT WORKS"
#         print request
#
#     print 'export outside if'
