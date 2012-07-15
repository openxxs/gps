from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('gps.apps.DataAnal.views',
    (r'^DataAnal/strain$','strain'),   
    (r'^DataAnal/crosssection$','crosssection'), 
    (r'^DataAnal/crosssectionAnalyse$','crosssectionAnalyse'),
    (r'^DataAnal/expandrate$','expandrate'), 
    (r'^DataAnal/expandrateAnalyse$','expandrateAnalyse'),
)
