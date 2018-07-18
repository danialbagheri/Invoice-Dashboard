# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from wiki.models import Wikientry
# Create your views here.
import markdown2
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def WikiView(request):
	#Reading the markdown file and rendering it
	md_entry = Wikientry.objects.filter(subject="NGINX")
	a = markdown2.markdown(md_entry[0].wiki_content)
	# Editing the markdown file
	if request.POST == 'POST':
		if request.GET.get('edit'):
			a = "ok"
	# rendering
	context = {
	"textholder" : a
	}
	return render(request, 'wiki.html', context=context)

# @login_required(login_url='/login/')
def WikiEdit(LoginRequiredMixin,request):
	login_url = '/login/'
	pass