from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns =patterns('gps.apps.DataProc.views',
    (r'^DataProc/bulkProcess/(?P<year_1>\w{4})/(?P<day_1>\w{3})/(?P<year_2>\w{4})/(?P<day_2>\w{3})/(?P<IGS>\w{4})$','bulkProcess'),
    (r'^DataProc/baseline$','baseline'),
    (r'^DataProc/baselineProcess$','baselineProcess'),
    (r'^DataProc/atmosphereProcess$','atmosphereProcess'),
    (r'^DataProc/ionosphere$','ionosphere'),
    (r'^DataProc/ionosphereProcess$','ionosphereProcess'),
    (r'^DataProc/highFrequencyData$','highFrequencyData'),
    (r'^DataProc/atmosphericDelay$','atmosphericDelay'),
    (r'^DataProc/datatrackrt$','datatrackrt'),
    (r'^DataProc/datatrack$','datatrack'),
    (r'^DataProc/trackProcess$','trackProcess'),
    (r'^DataProc/trackRTProcess$','trackRTProcess'),
    (r'^DataProc/trackRT_View$','trackRTView'),
    (r'^DataProc/killTrackRT$','killTrackRT'),
    (r'^DataProc/modifyConfigFile$','modifyConfigFile'),
    (r'^DataProc/writeConfigFile$','writeConfigFile'),
    (r'^DataProc/tableStatistic$','tableStatistic'),
    (r'^DataProc/initProcess$','initProcess'),
    (r'^DataProc/dataStatisticDetail$','dataStatisticDetail'),
    (r'^DataProc/tableStatisticDetail/(?P<filename>\w+\.?\w*)$','tableStatisticDetail'),
    (r'^DataProc/configEditDetail/(?P<filename>\w+\.?\w*)$','configEditDetail'),
    (r'^DataProc/configEdit$','configEdit'),
    (r'^DataProc/saveConfigFile/(?P<filename>\w+\.?\w*)$','saveConfigFile'),
    (r'^DataProc/resetConfigFile$','resetConfigFile'),
    (r'^DataProc/readGamitLog/(?P<year>\w{4})$','readGamitLog'),
)
