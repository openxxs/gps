from django.db import models

def _(msg):
    return msg
class Img(models.Model):
    name = models.CharField(max_length=10,null=True)
    img = models.ImageField(upload_to = 'static')
    class Meta:
        verbose_name = _('Img')
        verbose_name_plural = _('Imgs')

    def __unicode__(self):
        return self.name
# Create your models here.
class Site(models.Model):
    Code = models.CharField(max_length=10)
    Name = models.CharField(max_length=20)
    Longtitude = models.CharField(max_length=10,null=True)
    Latitude = models.CharField(max_length=10,null=True)
    Intro = models.CharField(max_length=300,null=True)
    ImgList = models.ManyToManyField(Img,null=True)
    
    class Meta:
            verbose_name = _('Site')
            verbose_name_plural = _('Sites')
    
    def __unicode__(self):
        return self.Name
    
