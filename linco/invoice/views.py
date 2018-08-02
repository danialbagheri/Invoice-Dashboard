# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from invoice.forms import InvoicesForm, SupplierForm
from django.shortcuts import render, redirect
from .models import Supplier, Invoices
from django.contrib import messages
# Create your views here.
# from django.views.generic import ListView
# from itertools import chain
def HomePage(request):
	return render(request, 'index.html', context={})

def SearchView(request):
	costs = 0
    # context['query'] = self.request.GET.get('q')
	query = request.POST.get('q', None)
	if query is not None:
		invoices_results = Invoices.objects.search(query)
		qs = invoices_results
		for i in qs:
			costs += i.invoice_value
		total = costs
		return render(request, 'search.html', context={"result": qs, "total": total})
	else:
		qs = Invoices.objects.none()
		return render(request, 'search.html', context={"result": qs})

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


def redir_to_invoicelist(request):
	return redirect('invoice_list', '1')
def invoice_list(request, page_num):
	NUM_ITEM_TO_SHOW = 30

	# pageview 
	if page_num == "":
		page_num = 1
	page_num = int(page_num)

	# get all the data and arrange them in date order
	a = Invoices.objects.all().order_by('-invoice_date')


	#slicing the result
	page_num -= 1
	start_slice= page_num * NUM_ITEM_TO_SHOW
	end_slice= start_slice + NUM_ITEM_TO_SHOW
	page_to_show = a[start_slice:end_slice]

	if len(page_to_show) <= 0:
		raise Http404("No result to show.")
	# Check if there is any more result to show on the next page
	start_slice += NUM_ITEM_TO_SHOW
	end_slice += NUM_ITEM_TO_SHOW
	next_page = a[start_slice:end_slice]
	if len(next_page) > 0:
		show_next_page = True
	else:
		show_next_page = False
	
	page_num += 1
	next_page_num = page_num + 1
	prev_page_num = page_num - 1

	#Decide to show the previous button or not
	if prev_page_num > 0:
		show_prev_page = True
	else:
		show_prev_page = False

	# Calculating the total invoice value of the display page
	costs = 0
	for i in page_to_show:
		costs += i.invoice_value
	page_total = costs

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
			context = {
				'result': page_to_show,
				'page_total': page_total,
				'page_num': page_num,
				'next_page_num': next_page_num,
				'prev_page_num': prev_page_num,
				'show_next_page': show_next_page,
				'show_prev_page': show_prev_page
			}
			return render(request, 'invoicelist.html', context)

	return render(request, 'invoicelist.html', context={'result': result})

def InvoiceView(request):
	previous_page = request.META.get('HTTP_REFERER')
	if request.method == 'GET':
		if request.GET.get('id'):
			product_id = request.GET['id']
			item = Invoices.objects.filter(id=product_id)
	return render(request, 'invoice.html', context={'item': item, 'prev_page': previous_page})


# JSON Date modules
from django.http import JsonResponse
import datetime
from json import JSONEncoder


def invoice_api(request):
	#calculate the spending of this month
	date = datetime.date.today()
	this_month = date.month
	this_year = date.year

	this_month_invoices = Invoices.objects.filter(
    invoice_date__month=this_month,
    invoice_date__year=date.year,
    organisation="Linco Care"
	)
	total_cost_month = 0
	for i in this_month_invoices:
		total_cost_month += i.invoice_value

	# Spending of this year
	this_year_invoices = Invoices.objects.filter(
	invoice_date__year=date.year,
	organisation="Linco Care"
	)
	total_cost_year = 0
	for i in this_year_invoices:
		total_cost_year += i.invoice_value
	
	data = {
		"total_cost_month": total_cost_month,
		"total_cost_year": total_cost_year,
		"this_month": this_month,
		"this_year": this_year
		}
	return JsonResponse(data, encoder=JSONEncoder)



