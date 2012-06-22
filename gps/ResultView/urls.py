from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('ResultView.views',
    (r'^ResultView/timeSeries$','timeSeries'),
    (r'^ResultView/velocities$','velocities'),
    (r'^ResultView/Draw_ts_pictures$','Draw_ts_pictures'),
    (r'^ResultView/baselineCheck$','baselineCheck'),
    (r'^ResultView/Draw_bs_pictures$','Draw_bs_pictures'),
    (r'^ResultView/atmosphereZenithDelay$','atmosphereZenithDelay'),
    (r'^ResultView/Draw_azDelay_pictures$','Draw_azDelay_pictures'),
    (r'^ResultView/resultApx$','resultApx'),
    (r'^ResultView/Draw_rApx_pictures$','Draw_rApx_pictures'),
)