from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    age = models.IntegerField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.username

