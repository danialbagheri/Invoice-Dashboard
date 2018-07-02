# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from invoice.forms import InvoicesForm, SupplierForm
from django.shortcuts import render
from .models import Supplier, Invoices
from django.contrib import messages
# Create your views here.
# from django.views.generic import ListView
# from itertools import chain
def HomePage(request):
	return render(request, 'index.html', context={})

def SearchView(request):
    # context['query'] = self.request.GET.get('q')
    query = request.POST.get('q', None)
    if query is not None:
    	invoices_results = Invoices.objects.search(query)
    	qs = invoices_results
    	return render(request, 'search.html', context={"result":qs})
    else:
    	qs = Invoices.objects.none()
    	return render(request, 'search.html', context={"result":qs})

def InvoiceUpload(request):
	if request.method == 'POST':
		form = InvoicesForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Invoice has been successfully recorded')
		else:
			form = InvoicesForm(request.POST)
			messages.error(request, 'Unfortunately your form submission was unsuccessful, please try again')
	else:
		form = InvoicesForm()

	return render(request,'invoiceform.html',context={"form":form})

def NewSupplier(request):
	if request.method == 'POST':
		form = SupplierForm(request.POST)
		if form.is_valid():
			print "form is valid"
			form.save()
			messages.success(request, 'Invoice has been successfully recorded')
		else:
			form = SupplierForm(request.POST)
			messages.error(request, 'Unfortunately your form submission was unsuccessful, please try again')
	else:
		form = SupplierForm()
	return render(request, 'newsupplier.html', context={"form":form})


def InvoiceList(request):
	if request.method == 'GET':
		if request.GET.get('filter_date'):
			filter_date = request.GET['filter_date']
			qyear = filter_date[:4]
			qmonth = filter_date[5:7]
			result = Invoices.objects.filter(invoice_date__month=qmonth,invoice_date__year=qyear).order_by('-invoice_date')
		elif request.GET.get('payment_method'):
			payment_method = request.GET['payment_method']
			result = Invoices.objects.filter(payment_method=payment_method).order_by('-invoice_date')
		elif request.GET.get('organisation'):
			organisation= request.GET['organisation']
			result = Invoices.objects.filter(organisation=organisation).order_by('-invoice_date')
		else:
			result = Invoices.objects.all().order_by('-invoice_date')

	return render(request, 'invoicelist.html', context={'result': result})

def InvoiceView(request):
	if request.method == 'GET':
		if request.GET.get('id'):
			product_id = request.GET['id']
			item = Invoices.objects.filter(id=product_id)
	return render(request, 'invoice.html', context={'item': item})	


