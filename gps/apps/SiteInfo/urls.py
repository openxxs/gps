from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('SiteInfo.views',
    (r'^SiteInfo/map$','Map'),
    (r'^SiteInfo/siteList$','sitesList'),
    (r'^SiteInfo/dataManaging$','dataManaging'),
    (r'^SiteInfo/log$','log'),
    (r'^SiteInfo/log/update_All$','update_All'),
    (r'^SiteInfo/siteBase/(?P<sitecode>\w{4})$','sitebase'),
    (r'^SiteInfo/data/(?P<sitecode>\w{4})$','data'),
    (r'^SiteInfo/data/siteSearch$','siteSearch'),
    (r'^SiteInfo/data/update/(?P<sitecode>\w{4})$','update'),
    (r'^SiteInfo/data/updateInfo$','updateInfo'),  
)
