from django.db import models
# Create your models here.

class userinfo(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField(null=True,blank=True)
    email=models.EmailField(null=True,blank=True)
    mobile=models.BigIntegerField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name