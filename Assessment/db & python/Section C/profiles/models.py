from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    age = models.IntegerField()
    bio = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.username

