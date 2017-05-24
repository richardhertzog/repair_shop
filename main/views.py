# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Service
from .forms import ServiceForm

# Create your views here.
def index(request):
    # print 'request', request.GET
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

# def import_csv(request):
#     print 'import beginning'
#     if(request.POST.post('import')):
#         print "IMPORT WORKS"
#         print request
#
#     print request
#
# def export_csv(request):
#     print 'export beginning'
#     if(request.POST.post('export')):
#         print "EXPORT WORKS"
#         print request
#
#     print 'export outside if'
