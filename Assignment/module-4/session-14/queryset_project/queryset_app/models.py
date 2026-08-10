from django.db import models


# ==================================================
# TASK 1
# ==================================================

class Restaurant(models.Model):

    name = models.CharField(
        max_length=200
    )

    cuisine = models.CharField(
        max_length=100
    )

    rating = models.FloatField()


    def __str__(self):

        return self.name


# ==================================================
# TASK 3
# ==================================================

class Movie(models.Model):

    name = models.CharField(
        max_length=200
    )


    def __str__(self):

        return self.name


class Review(models.Model):

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    review_text = models.TextField()

    rating = models.IntegerField()


    def __str__(self):

        return f"Review for {self.movie.name}"


# ==================================================
# TASK 4 & TASK 5
# ==================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100
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

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )


    def __str__(self):

        return self.name