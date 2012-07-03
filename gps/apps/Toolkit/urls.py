from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns +=patterns('Toolkit.views',
    (r'^Toolkit/doy$','doy'),
    (r'^Toolkit/transformDoy$','transformDoy'),
    (r'^Toolkit/framework$','framework'),
    (r'^Toolkit/changeFrame$','changeFrames'),
    (r'^Toolkit/dataDownload$','dataDownloads'),
    (r'^Toolkit/dataDownloadProcess$','dataDownloadProcess'),
)