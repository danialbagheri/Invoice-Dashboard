# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from invoice.models import Invoices, Supplier
import datetime

class InvoicesForm(ModelForm):

	ORGANISATION = (
		("Linco Care","Linco Care"),
		("QHorizons", "QHorizons"),
	)

	PAYMENT_CHOICES = (
		('Credit Card', 'Credit Card'),
		('Bank Transfer', 'Bank Transfer'),
		('Cheque', 'Cheque'),
		('Cash', 'Cash'),
	)
	EXPENSE_TYPE= (
		('Stationary', 'Stationary'),
		('IT', 'IT'),
		('PR and Social Media', 'PR and Social Media'),
		('Marketing', 'Marketing'),
		('Equipment', 'Equipment'),
		('Transport', 'Transport'),
		('Maintenance', 'Maintenance'),
		('Print', 'Print'),
		('Others', 'Others'),
	)
	CURRENCY = (
		(u'£', 'British Pound'),
		(u'$', 'United States Dollar'),
		(u'€', 'EURO'),
	)


	organisation = forms.ChoiceField(
		label = ('organisation'),
		required = True,
		choices = ORGANISATION,
		widget = forms.Select(attrs = {'class': 'form-control'})
		)
	supplier_name = forms.ModelChoiceField(
		queryset = Supplier.objects.all(),
		initial=0,
		widget = forms.Select(attrs = {'class': 'form-control'})
		)
	invoice_date = forms.DateField(
		initial=datetime.date.today,
		required= False,
		widget = forms.SelectDateWidget(attrs = {'class': 'custom-select'})
		)
	invoice = forms.FileField(
		label = ('Upload Screenshot'), 
		required = False,
		help_text = 'Upload a the invoice',
		widget = forms.FileInput(attrs = {'class': 'form-control-file'})
		)
	payment_method = forms.ChoiceField(
		label = ('payment_method'),
		required = True,
		choices = PAYMENT_CHOICES,
		widget = forms.Select(attrs = {'class': 'form-control'})
		)
	expense_type = forms.ChoiceField(
		label = ('expense_type'),
		required = True,
		choices = EXPENSE_TYPE,
		widget = forms.Select(attrs = {'class': 'form-control'})
		)
	refund = forms.BooleanField(
		label = ('refund'),
		required = False,
		widget = forms.CheckboxInput(attrs = {'class': 'form-check'})
		)
	currency = forms.ChoiceField(
		label = ('currency'),
		required = True,
		choices = CURRENCY,
		widget = forms.Select(attrs = {'class': 'form-control'})
		)
	purchased_item = forms.CharField(
		label = 'purchased_item',
		max_length=400,
		required = True,
		widget = forms.TextInput(attrs = {'class': 'form-control'})
		)
	class Meta:
		model = Invoices
		fields = (
		    'organisation',
		    'supplier_name',
		    'purchased_item',
		    'invoice_date',
		    'invoice',
		    'invoice_value',
			'vat_amount',
		    'payment_method',
		    'expense_type',
		    'refund',
		    'currency',
		)

class SupplierForm(ModelForm):
	
	supplier_name = forms.CharField(
		label = ('Supplier Name'),
		required = True,
		help_text = 'This is the company you have purchased from.',
		widget = forms.TextInput(attrs = {'class': 'form-control'})
	)
	vat_number = forms.CharField(
		label = ('Vat Number'),
		required = False,
		widget = forms.TextInput(attrs = {'class': 'form-control'})
	)

	class Meta:
		model = Supplier
		fields = (
			'supplier_name',
			'vat_number',
		)




