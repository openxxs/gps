from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('gps.apps.Toolkit.views',
    (r'doy$','doy'),
    (r'transformDoy$','transformDoy'),
    (r'framework$','framework'),
    (r'changeFrame$','changeFrames'),
    (r'dataDownload$','dataDownloads'),
    (r'dataDownloadProcess$','dataDownloadProcess'),
)
