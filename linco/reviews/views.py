from __future__ import division

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
import requests
import pprint
from django.http import Http404

from operator import itemgetter

import datetime
from dateutil.parser import parse

from django.core.paginator import Paginator


'''
NOTES:

Rob says: I think we should rethink the url structure for the reviews. seems odd to have /reviews/brands/ then have a query string with brand in it.

'''


# Create your views here.
def chooseBrand(request):

	brands_resp = requests.get("http://localhost:9999/brands/")
	all_brands = json.loads(brands_resp.text)

	context = {
		"all_brands": all_brands,
	}
	return render(request, "reviews/choosebrand.html", context=context)



def showReviews(request):

	NUM_REVIEWS_TO_SHOW = 10

	# get product, brand, sort/filter and page number from query string 
	# (vars that end in _qs are querystring)
	product_qs = request.GET.get('product')
	if product_qs == None:
		product_qs = ""
	brand_qs = request.GET.get('brand')
	if brand_qs == None:
		brand_qs = ""
	
	sort_on_qs = request.GET.get('sort')
	page_num_qs = request.GET.get('page')
	if page_num_qs == None:
		page_num_qs = 1
	else:
		page_num_qs = int(page_num_qs)
	
	# Do reviews api request to get reviews. Filter on brand and product
	# reviews_resp = requests.get("http://localhost:5000/reviews/?brand=%s&product=%s" % (brand_qs, product_qs))
	reviews_resp = requests.get("https://api.lincocare.co.uk/reviews/?brand=%s&product=%s" % (brand_qs, product_qs))
	reviews = json.loads(reviews_resp.text)
	

	# sort reviews depending on sort query string
	reviews_to_sort = []
	for review in reviews:
		current_date = datetime.datetime.strptime( reviews[review]['date_added'], "%a, %d %b %Y %X %Z")
		# add date in iso form
		reviews[review]['date_added_iso'] = current_date.isoformat()
		# add id as an attribute rather than the list index
		reviews[review]['id'] = review
		reviews_to_sort.append(reviews[review])

	if sort_on_qs == "unpublished":
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['approved'])
	elif sort_on_qs == "published":
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['approved'], reverse=True)
	elif sort_on_qs == "recent":
		# sort on date
		# date string cheat sheet: http://strftime.org/
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: datetime.datetime.strptime( k['date_added'], "%a, %d %b %Y %X %Z" ), reverse=True)
	elif sort_on_qs == "rating":
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['score'], reverse=True)
	elif sort_on_qs == "helpful":
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: k['upvotes'] - k['downvotes'], reverse=True)
	else:
		# default sort by date
		reviews_sorted = sorted(reviews_to_sort, key=lambda k: datetime.datetime.strptime( k['date_added'], "%a, %d %b %Y %X %Z" ), reverse=True)

	
	# paginate
	p = Paginator(reviews_sorted, NUM_REVIEWS_TO_SHOW)

	this_pages_reviews = p.page(page_num_qs)


	
	# Get brands from product api
	# products api is on localhost:9999
	brands_resp = requests.get("http://localhost:9999/brands/")
	all_brands = json.loads(brands_resp.text)

	
	# Get all products for current brand
	# Do another API request without filtering on brand, or else the products will be restricted
	response_filtered_on_brand = requests.get("https://api.lincocare.co.uk/reviews/?brand=%s" % (brand_qs))
	# response_filtered_on_brand = requests.get("http://localhost:5000/reviews/?brand=%s" % (brand_qs))
	rev_filtered_on_brand = json.loads(response_filtered_on_brand.text)
	# get all products for current brand for the dropdown at the top
	products_for_current_brand = set()
	for x in rev_filtered_on_brand:
		products_for_current_brand.add(rev_filtered_on_brand[x]['product'])

	context = {
	"this_pages_reviews": this_pages_reviews,
	"product": product_qs,
	"products_for_current_brand": products_for_current_brand,
	"brand": brand_qs,
	"all_brands": all_brands,
	"sort_on": sort_on_qs,
	}
	return render(request, "reviews/showreviews.html", context=context)

def stats(request):

	# get product filter from query string
	product_qs = request.GET.get('product')
	if product_qs == None:
		product_qs = ""
	brand_qs = request.GET.get('brand')
	if brand_qs == None or brand_qs == "all":
		brand_qs = ""
	# do api request to get reviews with filters

	response = requests.get("https://api.lincocare.co.uk/reviews/?brand=%s&product=%s" % (brand_qs, product_qs))
	# response = requests.get("http://localhost:5000/reviews/?brand=%s&product=%s" % (brand_qs, product_qs))
	reviews = json.loads(response.text)

	# process reviews to get 
	# 	- num reviews
	#	- percentages of each stars
	# 	- num of each stars
	num_reviews = len(reviews)

	cumulative_scores = 0
	
	scores_count = [0,0,0,0,0]
	for x,y in reviews.items():
		# Count of 1, 2, 3, 4 and 5 stars respectively within reviews
		scores_count[y["score"]-1] += 1
		# Add all scores for using later to work out general score average
		cumulative_scores += y["score"]
	


	if num_reviews == 0:
		scores_count = [0,0,0,0,0]
		scores_percentages = [0,0,0,0,0]
		scores_info = zip(scores_count, scores_percentages)
		overall_average = 0
	else:
		scores_percentages = [ (x/num_reviews)*100 for x in scores_count ]
		scores_info = zip(scores_count, scores_percentages)
		scores_info.reverse()
		overall_average = cumulative_scores/num_reviews


	# Get all products for current brand from products api
	prod_resp = requests.get("http://localhost:9999/products/?brand=%s" % (brand_qs))
	prod_for_current_brand_all_info = json.loads(prod_resp.text)
	products_for_current_brand = []
	for prods in prod_for_current_brand_info:
	 	products_for_current_brand.append(prods['name'])

	# get all brands from products api
	brands_resp = requests.get("http://localhost:9999/brands/")
	all_brands = json.loads(brands_resp.text)

	context = {
		"brand": brand_qs,
		"product": product_qs,
		"overall_average": overall_average,
		"num_reviews": num_reviews,
		"scores_info": scores_info,
		"all_brands": all_brands,
		"products_for_current_brand": products_for_current_brand,
	}
	
	return render(request, "reviews/stats.html", context=context)










