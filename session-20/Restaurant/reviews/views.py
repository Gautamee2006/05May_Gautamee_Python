from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from restaurants.models import Restaurant
from .models import Review

@login_required
def add_review_view(request, restaurant_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        # Check if user already reviewed
        existing_review = Review.objects.filter(user=request.user, restaurant=restaurant).first()
        if existing_review:
            messages.error(request, "You have already reviewed this restaurant.")
            return redirect('restaurant_detail', restaurant_id=restaurant.id)

        try:
            rating = int(request.POST.get('rating', 5))
            comment = request.POST.get('comment', '').strip()

            if not (1 <= rating <= 5):
                messages.error(request, "Rating must be between 1 and 5 stars.")
                return redirect('restaurant_detail', restaurant_id=restaurant.id)

            if not comment:
                messages.error(request, "Please enter a comment for your review.")
                return redirect('restaurant_detail', restaurant_id=restaurant.id)

            Review.objects.create(
                user=request.user,
                restaurant=restaurant,
                rating=rating,
                comment=comment
            )

            # Update aggregate rating on restaurant
            avg_rating = Review.objects.filter(restaurant=restaurant).aggregate(Avg('rating'))['rating__avg']
            total_revs = Review.objects.filter(restaurant=restaurant).count()

            restaurant.rating = round(avg_rating, 2) if avg_rating else 0.00
            restaurant.total_reviews = total_revs
            restaurant.save()

            messages.success(request, "Thank you for your review! ⭐")
        except Exception as e:
            messages.error(request, f"Error saving review: {str(e)}")

    return redirect('restaurant_detail', restaurant_id=restaurant_id)
