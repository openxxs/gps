from django.conf import settings
import os
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer


handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^DataAnal/", include("DataAnal.urls")),
    url(r"^DataProc/", include("DataProc.urls")),
    url(r"^ResultView/", include("ResultView.urls")),
    url(r"^SiteInfo/", include("SiteInfo.urls")),
    url(r"^Toolkit/", include("Toolkit.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
)

urlpatterns +=patterns('', 
    (r'^exp2nd/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'exp2nd')}),
    (r'^data_download/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'data_download')}),
    (r'^track/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'track')}),
    (r'^log/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'log')}),
    (r'^site_list/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'site_list')}),
    (r'^css/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'templates/css')}),
    (r'^js/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'templates/js')}),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'templates/images')}),
    (r'^amstock/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'templates/amstock')}),
    (r'^base/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(os.path.dirname(__file__),'templates/base')}),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )
