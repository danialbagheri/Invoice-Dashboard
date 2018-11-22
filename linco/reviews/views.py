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

# reviews_api_url = "http://localhost:5000"
reviews_api_url = "https://api.lincocare.co.uk"
products_api_url = "http://localhost:9999"

# Create your views here.
def chooseBrand(request):

	brands_resp = requests.get(products_api_url + "/brands/")
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

	# Get the product category ids by for the products of the current brand (if any) through the product API.
	products_resp = requests.get(products_api_url+"/product-categories/?brand=%s" % (brand_qs))

	products_for_current_brand = json.loads(products_resp.text)
	product_category_ids = []
	product_dropdown_info = []
	for pr in products_for_current_brand:
	 	product_category_ids.append(pr["id"])
	 	product_dropdown_info.append((pr["id"], pr["name"]))

	product_category_ids_for_qs = ",".join(product_category_ids)
	
	# if there's a product query string, just get reviews of that product. Otherwise use product_category_ids_for_qs which will have all the products for the current brand
	if product_qs:
		reviews_resp = requests.get(reviews_api_url+"/reviews/?product=%s" % (product_qs))
		# reviews_resp = requests.get("https://api.lincocare.co.uk/reviews/?product=%s" % (product_qs))
	else:
		# PLEASE NOTE: THIS WILL MALFUNCTION IF THERE'S NO PRODUCTS CATEGORY IDS RETURNED FOR THIS BRAND BY THE PRODUCTS API. The product query string will be empty so it will show all the reviews. TO COMBAT THIS, WILL HAVE TO MAKE SURE THERE'S AT LEAST ONE PRODUCT CATEGORY FOR EACH BRAND.
		# TODO: Think of alternative to this workaround !!!
		reviews_resp = requests.get(reviews_api_url+"/reviews/?product=%s" % (product_category_ids_for_qs))
		# reviews_resp = requests.get("https://api.lincocare.co.uk/reviews/?product=%s" % (product_category_ids_for_qs))

	reviews = json.loads(reviews_resp.text)
	
	# sort reviews depending on sort query string
	sort_on_qs = request.GET.get('sort')
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


	# Get the product names for each of these reviews
	for rr in reviews_sorted:
		cat_id = rr["product_category_id"]
		respp = requests.get(products_api_url+"/product-categories/{}/".format(cat_id))
		tt = json.loads(respp.text)
		rr["product_category_name"] = tt["name"]
	

	# paginate
	page_num_qs = request.GET.get('page')
	if page_num_qs == None:
		page_num_qs = 1
	else:
		page_num_qs = int(page_num_qs)

	p = Paginator(reviews_sorted, NUM_REVIEWS_TO_SHOW)

	this_pages_reviews = p.page(page_num_qs)

	context = {
	"this_pages_reviews": this_pages_reviews,
	"product_qs": product_qs,
	"product_dropdown_info": product_dropdown_info,
	"brand": brand_qs,
	"sort_on": sort_on_qs,
	"reviews_api_url": reviews_api_url,
	}
	return render(request, "reviews/showreviews.html", context=context)



def stats(request):


	# get product, brand, sort/filter and page number from query string 
	# (vars that end in _qs are querystring)
	product_qs = request.GET.get('product')
	if product_qs == None:
		product_qs = ""
	brand_qs = request.GET.get('brand')
	if brand_qs == None:
		brand_qs = ""
	

	# Get brands from product api
	# products api is on localhost:9999
	brands_resp = requests.get(products_api_url+"/brands/")
	all_brands = json.loads(brands_resp.text)

	# Get the product category ids by for the products of the current brand (if any) through the product API.
	products_resp = requests.get(products_api_url+"/product-categories/?brand=%s" % (brand_qs))
	products_for_current_brand = json.loads(products_resp.text)
	product_category_ids = []
	product_dropdown_info = []
	for pr in products_for_current_brand:
	 	product_category_ids.append(pr["id"])
	 	product_dropdown_info.append((pr["id"], pr["name"]))

	product_category_ids_for_qs = ",".join(product_category_ids)

	# if there's a product query string, just get reviews of that product. Otherwise use product_category_ids_for_qs which will have all the products for the current brand
	if product_qs:
		reviews_resp = requests.get(reviews_api_url+"/reviews/?product=%s" % (product_qs))
	else:
		reviews_resp = requests.get(reviews_api_url+"/reviews/?product=%s" % (product_category_ids_for_qs))

	reviews = json.loads(reviews_resp.text)
	

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



	context = {
		"all_brands": all_brands,
		"brand_qs": brand_qs,
		"overall_average": overall_average,
		"num_reviews": num_reviews,
		"scores_info": scores_info,
		"product_dropdown_info": product_dropdown_info,
	}
	
	return render(request, "reviews/stats.html", context=context)










