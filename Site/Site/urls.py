from django.conf.urls import patterns, include, url
from django.contrib import admin
from priceQuery.views import getList,addNewQuery,getData
from products.views import searchProduct
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^getlist/$', getList),
	url(r'^newquery/$',addNewQuery),
	url(r'^query/key/(\w+)/$',getData),
	url(r'^search/$',searchProduct),
    url(r'^admin/', include(admin.site.urls)),
)
