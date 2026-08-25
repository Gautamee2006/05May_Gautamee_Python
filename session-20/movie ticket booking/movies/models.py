from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    poster = models.URLField(max_length=500, default="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=600&auto=format&fit=crop&q=80")
    rating = models.FloatField(default=4.0, help_text="Rating out of 5.0")

    def clean(self):
        if not self.title or not self.title.strip():
            raise ValidationError("Movie title cannot be empty.")
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0.0 and 5.0.")

    def __str__(self):
        return f"{self.title} ({self.language})"


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    date = models.DateField()
    time = models.TimeField()
    screen_name = models.CharField(max_length=50, default="Screen 1")
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)

    def clean(self):
        if self.ticket_price <= 0:
            raise ValidationError("Ticket price must be greater than 0.")

    def get_booked_seats_list(self):
        """Returns a list of seat names currently booked for this active show."""
        active_bookings = self.bookings.filter(status='Confirmed')
        booked_seats = []
        for b in active_bookings:
            seats = [s.strip() for s in b.selected_seats.split(',') if s.strip()]
            booked_seats.extend(seats)
        return booked_seats

    def __str__(self):
        return f"{self.movie.title} | {self.date} at {self.time.strftime('%I:%M %p')} ({self.screen_name})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    selected_seats = models.CharField(max_length=255, help_text="Comma separated list of seats, e.g. A1, A2")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = 'BK' + str(uuid.uuid4().hex[:6]).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username} - {self.movie.title}"
