# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from wiki.models import Wikientry
# Create your views here.
import markdown2


def WikiView(request):
	#Reading the markdown file and rendering it
	md_entry = Wikientry.objects.filter(subject="NGINX")
	a = markdown2.markdown(md_entry[0].wiki_content)
	# Editing the markdown file
	# if request.POST == GET
	# rendering
	context = {
	"textholder" : a
	}
	return render(request, 'wiki.html', context=context)
