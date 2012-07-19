from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('gps.apps.SiteInfo.views',
    (r'map$','Map'),
    (r'siteList$','sitesList'),
    (r'dataManaging$','dataManaging'),
    (r'log/update_All$','update_All'),
    (r'siteBase/(?P<sitecode>\w{4})$','sitebase'),
    (r'siteBase$','sitebase'),
    (r'data/(?P<sitecode>\w{4})$','data'),
    (r'data/siteSearch$','siteSearch'),
    (r'data/update/(?P<sitecode>\w{4})$','update'),
    (r'data/updateInfo$','updateInfo'),  
)
