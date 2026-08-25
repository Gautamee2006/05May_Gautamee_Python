from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from reviews.models import Review
from restaurants.models import Restaurant
from admin_panel.decorators import staff_required


@staff_required
def review_list(request):
    restaurant_filter = request.GET.get('restaurant', '')
    visibility_filter = request.GET.get('visibility', '')
    rating_filter = request.GET.get('rating', '')

    reviews = Review.objects.select_related('user', 'restaurant').order_by('-created_at')

    if restaurant_filter:
        reviews = reviews.filter(restaurant_id=restaurant_filter)
    if visibility_filter == 'visible':
        reviews = reviews.filter(is_visible=True)
    elif visibility_filter == 'hidden':
        reviews = reviews.filter(is_visible=False)
    if rating_filter:
        reviews = reviews.filter(rating=rating_filter)

    context = {
        'reviews': reviews[:200],
        'restaurants': Restaurant.objects.filter(is_active=True),
        'restaurant_filter': restaurant_filter,
        'visibility_filter': visibility_filter,
        'rating_filter': rating_filter,
        'page_title': 'Reviews & Ratings',
        'active_nav': 'reviews',
    }
    return render(request, 'admin_panel/reviews/list.html', context)


@staff_required
def review_toggle(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.is_visible = not review.is_visible
        review.save()
        status = 'shown' if review.is_visible else 'hidden'
        messages.success(request, f"Review by '{review.user.username}' is now {status}.")
    return redirect('panel_review_list')


@staff_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        username = review.user.username
        review.delete()
        messages.success(request, f"Review by '{username}' deleted.")
    return redirect('panel_review_list')
