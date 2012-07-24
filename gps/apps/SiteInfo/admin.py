from django.contrib import admin
from models import Img,Site

class SiteAdmin(admin.ModelAdmin):
    pass

class ImgAdmin(admin.ModelAdmin):
    pass

admin.site.register(Site,SiteAdmin)
admin.site.register(Img,ImgAdmin)