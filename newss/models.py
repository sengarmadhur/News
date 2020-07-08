from django.db import models


# Create your models here.

class News(models.Model):
    name = models.CharField(max_length=50)
    summary = models.TextField()
    body = models.TextField()
    date = models.DateField()
    pic = models.TextField()
    picurl = models.FileField(default="-")
    author = models.CharField(default='-',max_length=250)
    ocatid = models.IntegerField(default=0)
    catname = models.CharField(default="-",max_length=250)
    catid = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    tags = models.TextField(default="")
    act = models.IntegerField(default=0)
    rand = models.IntegerField(default=0)

    def __str__(self):
        return self.name
