from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.views import otp_verified_required
from .models import Movie, Show, Booking

def movie_list_view(request):
    query = request.GET.get('q', '').strip()
    selected_genre = request.GET.get('genre', '').strip()
    selected_language = request.GET.get('language', '').strip()

    movies = Movie.objects.all()

    if query:
        movies = movies.filter(title__icontains=query)

    if selected_genre:
        movies = movies.filter(genre__iexact=selected_genre)

    if selected_language:
        movies = movies.filter(language__iexact=selected_language)

    # Get filter choices dynamically
    all_genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    all_languages = Movie.objects.values_list('language', flat=True).distinct().order_by('language')

    context = {
        'movies': movies,
        'query': query,
        'selected_genre': selected_genre,
        'selected_language': selected_language,
        'all_genres': all_genres,
        'all_languages': all_languages,
    }
    return render(request, 'movies/movie_list.html', context)


def movie_detail_view(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    shows = movie.shows.all().order_by('date', 'time')
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'shows': shows})


@otp_verified_required
def seat_selection_view(request, show_id):
    show = get_object_or_404(Show, pk=show_id)
    booked_seats = show.get_booked_seats_list()

    # Generate seats matrix: Rows A, B, C, D with 5 seats each (A1-A5, B1-B5, C1-C5, D1-D5)
    rows = ['A', 'B', 'C', 'D']
    seat_matrix = []
    for r in rows:
        row_seats = []
        for i in range(1, 6):
            seat_code = f"{r}{i}"
            row_seats.append({
                'code': seat_code,
                'is_booked': seat_code in booked_seats
            })
        seat_matrix.append({'row': r, 'seats': row_seats})

    context = {
        'show': show,
        'movie': show.movie,
        'seat_matrix': seat_matrix,
        'booked_seats': booked_seats,
    }
    return render(request, 'movies/seat_selection.html', context)


@otp_verified_required
def book_ticket_view(request, show_id):
    show = get_object_or_404(Show, pk=show_id)

    if request.method == 'POST':
        seats_str = request.POST.get('selected_seats', '').strip()

        if not seats_str:
            messages.error(request, "Please select at least one seat to proceed.")
            return redirect('seat_selection', show_id=show.id)

        selected_list = [s.strip().upper() for s in seats_str.split(',') if s.strip()]
        if not selected_list:
            messages.error(request, "Invalid seat selection.")
            return redirect('seat_selection', show_id=show.id)

        # Check for double booking
        already_booked = show.get_booked_seats_list()
        conflicts = [seat for seat in selected_list if seat in already_booked]
        if conflicts:
            messages.error(request, f"Seat(s) {', '.join(conflicts)} have just been booked. Please choose available seats.")
            return redirect('seat_selection', show_id=show.id)

        # Calculate total price
        total_amount = len(selected_list) * show.ticket_price

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            movie=show.movie,
            show=show,
            selected_seats=', '.join(selected_list),
            total_amount=total_amount,
            status='Confirmed'
        )

        messages.success(request, f"Ticket booked successfully! Booking ID: {booking.booking_id}")
        return redirect('booking_confirmation', booking_id=booking.booking_id)

    return redirect('seat_selection', show_id=show.id)


@otp_verified_required
def booking_confirmation_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'movies/booking_confirmation.html', {'booking': booking})


@otp_verified_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'movies/my_bookings.html', {'bookings': bookings})


@otp_verified_required
def booking_detail_view(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    return render(request, 'movies/booking_detail.html', {'booking': booking})
