from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

