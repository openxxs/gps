from django.db import models
from gps.config import CONFIG
def _(msg):
    return msg
class Img(models.Model):
    name = models.CharField(max_length=10,null=True,blank=True)
    img = models.ImageField(upload_to = CONFIG.SOFTWAREPATH+'/site_media/static/img/')
    class Meta:
        verbose_name = _('Img')
        verbose_name_plural = _('Imgs')

    def __unicode__(self):
        return self.name
# Create your models here.
class Site(models.Model):
    Code = models.CharField(max_length=10)
    Name = models.CharField(max_length=20)
    Longtitude = models.CharField(max_length=10,null=True,blank=True)
    Latitude = models.CharField(max_length=10,null=True,blank=True)
    Intro = models.CharField(max_length=300,null=True,blank=True)
    ImgList = models.ManyToManyField(Img,null=True,blank=True)
    
    class Meta:
            verbose_name = _('Site')
            verbose_name_plural = _('Sites')
    
    def __unicode__(self):
        return self.Name
    
