from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('DataAnal.views',
    (r'^DataAnal/strain$','strain'),   
    (r'^DataAnal/crosssection$','crosssection'), 
    (r'^DataAnal/crosssectionAnalyse$','crosssectionAnalyse'),
    (r'^DataAnal/expandrate$','expandrate'), 
    (r'^DataAnal/expandrateAnalyse$','expandrateAnalyse'),
    (r'^DataAnal/deltaV$','deltaV'),
    (r'^DataAnal/deltaS$','deltaS'),
)
