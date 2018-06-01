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


	organisation = forms.ChoiceField(
		label = ('organisation'),
		required = True,
		choices = ORGANISATION,
		widget = forms.Select(attrs = {'class': 'form-control'})
		)
	invoice_date = forms.DateField(
		required= False,
		widget = forms.SelectDateWidget(attrs = {'class': 'form-control','type':'date','value':'2018-06-19'})
		)
	invoice = forms.FileField(
		label = ('Upload Screenshot'), 
		required = False,
		help_text = 'Upload a the invoice',
		widget = forms.FileInput(attrs = {'class': 'form-control-file'})
		)

	class Meta:
		model = Invoices
		fields = (
		    'organisation',
		    'supplier_name',
		    'invoice_date',
		    'invoice',
		    'invoice_value',
		)

class SupplierForm(ModelForm):
	
	supplier_name = forms.CharField(
		label = ('Supplier Name'),
		required = True,
		help_text = 'This is the company you have purchased from.',
		widget = forms.TextInput(attrs = {'class': 'form-control'})
	)
	vat_number = forms.IntegerField(
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




