from django.db import models

# Create your models here.

class article(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=500)
    bodylong = models.TextField(default='-')
    fb = models.CharField(default = '-',max_length=50)
    tw = models.CharField(default='-',max_length=50)
    insta = models.CharField(default='-',max_length=50)
    ph = models.CharField(default="999999",max_length=12)
    picname = models.TextField(default="")
    picurl = models.TextField(default="")
    picname2 = models.TextField(default="")
    picurl2 = models.TextField(default="")

    def __str__(self):
        return self.title + " | "+str(self.pk)
