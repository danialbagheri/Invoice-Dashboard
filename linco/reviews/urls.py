from django.conf.urls import url
from . import views

app_name = 'reviews'

urlpatterns = [
    url(r'^$', views.chooseBrand, name='index'),
	url(r'^stats/$', views.reviewStats, name='review_stats'),
	url(r'^brands/$', views.showReviews, name='show_reviews'),
]