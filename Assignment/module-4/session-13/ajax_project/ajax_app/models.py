from django.db import models


class Song(models.Model):

    name = models.CharField(
        max_length=200
    )

    artist = models.CharField(
        max_length=200
    )


    def __str__(self):

        return self.name


class Product(models.Model):

    name = models.CharField(
        max_length=200
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    def __str__(self):

        return self.name


class Movie(models.Model):

    name = models.CharField(
        max_length=200
    )

    genre = models.CharField(
        max_length=100
    )


    def __str__(self):

        return self.name


class Playlist(models.Model):

    name = models.CharField(
        max_length=200
    )


    def __str__(self):

        return self.name