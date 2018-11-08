"""linco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from invoice.views import *
from wiki.views import *
from django.contrib.auth.views import login, logout
from accounts.views import *
from django.http import HttpResponse


# handler404 = 'blog.views.page_not_found_view'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePage, name='home'),
    url(r'^search$', SearchView, name='search'),
    url(r'^submit/$', InvoiceUpload, name='invoice-upload'),
    url(r'^newsupplier$', NewSupplier, name='new-supplier'),
    url(r'^invoicelist$', redir_to_invoicelist, name='InvoiceList'),
    url(r'^invoicelist/(?P<page_num>\d+)/$',
        invoice_list, name='invoice_list'),
    url(r'^invoice$', InvoiceView, name='Invoice'),
    url(r'^invoice-api/$', invoice_api, name='invoice-api'),
    url(r'^wiki$',wikihome, name='wikihome'),
    url(r'^wiki/(?P<id>\d+)/$',wikiview, name='wikiview'),
    url(r'^login$', login, {'template_name':'accounts/login.html'}, name='login'),
    url(r'^logout$', logout, {'template_name':'accounts/logout.html'}, name='logout'),
    url(r'^register$',register, name='register'),
    url(r'^accounts/profile/$',profile, name='profile'),
    url(r'^wiki/edit$',WikiEdit, name='Wiki_edit'),
    url(r'^reviews/', include('reviews.urls'), name='reviews'),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
