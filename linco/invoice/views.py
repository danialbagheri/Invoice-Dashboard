# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Supplier, Invoices
# Create your views here.
# from django.views.generic import ListView
# from itertools import chain

def SearchView(request):
    # context['query'] = self.request.GET.get('q')
    query = request.POST.get('q', None)
    if query is not None:
    	invoices_results = Invoices.objects.search(query)
    	qs = invoices_results
    	return render(request, 'search.html', context={"result":qs})
    else:
    	qs =  Invoices.objects.none()
    	return render(request, 'search.html', context={"result":qs})

    