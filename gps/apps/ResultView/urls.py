from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('gps.apps.ResultView.views',
    (r'timeSeries$','timeSeries'),
    (r'velocities$','velocities'),
    (r'Draw_ts_pictures$','Draw_ts_pictures'),
    (r'baselineCheck$','baselineCheck'),
    (r'Draw_bs_pictures$','Draw_bs_pictures'),
    (r'atmosphereZenithDelay$','atmosphereZenithDelay'),
    (r'Draw_azDelay_pictures$','Draw_azDelay_pictures'),
    (r'resultApx$','resultApx'),
    (r'Draw_rApx_pictures$','Draw_rApx_pictures'),
)