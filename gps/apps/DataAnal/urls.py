from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('gps.apps.DataAnal.views',
    (r'strain$','strain'),   
    (r'crosssection$','crosssection'), 
    (r'crosssectionAnalyse$','crosssectionAnalyse'),
    (r'expandrate$','expandrate'), 
    (r'expandrateAnalyse$','expandrateAnalyse'),
)
