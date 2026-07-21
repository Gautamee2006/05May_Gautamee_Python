from django.db import models

# Create your models here.
class Cuisine(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField()

    def __str__(self):
        return self.name
    
class Restaurant(models.Model):
    name=models.CharField(max_length=20)
    location=models.CharField(max_length=20)
    rating=models.FloatField()

    cuisine=models.ForeignKey(Cuisine,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name
    
