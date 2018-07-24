# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from wiki.models import Wikientry, Category
# Create your views here.
import markdown2
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def wikihome(request):
	category = Category.objects.all()
	wikientry = Wikientry.objects.all()
	# def get_queryset_data(self):
	# 	Categoryname = category.name
	# 	self.categoryname = categoryname
	# 	categorynames = list(map(lambda c: c.name, category.get_sub_categorys()))
	# 	wikientry = objects.filter(category__name__in=categorynames)
	# 	pass
	# wikientry = category_queryset__Wikientry()

	# categories = {}
	# sub_categories = []
	# for category in category_queryset:
	# 	if category.parent is None:
	# 		parent = category.category_name
	# 		child = []

	# 		for item in category_queryset:
	# 			if str(item.parent) == parent:
	# 				child.append(item.category_name)
	# 			categories[parent]=child

	# 		sub_categories = []
	# 		for item in category_queryset:
	# 			if item.parent == category.parent:
	# 				sub_categories.append(item.category_name)


	context = {
	"category": category,
	"wikientry": wikientry
	}
	return render(request, 'wiki.html', context)

def wikiview(request, id):
	#Reading the markdown file and rendering it
	# md_entry = Wikientry.objects.get(subject="NGINX")
	md_entry = get_object_or_404(Wikientry, id=id)
	a = markdown2.markdown(md_entry.wiki_content)

	# rendering
	context = {
	"textholder" : a
	}
	return render(request, 'wiki/wikiview.html', context)

# @login_required(login_url='/login/')
def WikiEdit(LoginRequiredMixin,request, id=None):
	login_url = '/login/'
	instance = get_object_or_404(Post, id=id)
	context = {
		"form" : form,
	}
	pass