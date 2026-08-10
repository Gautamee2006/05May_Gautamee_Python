from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Order, Product, Movie, Review, Playlist
from .forms import ProductForm, ReviewForm


def custom_permission_denied(request, exception=None):
    """Custom HTTP 403 Permission Denied view."""
    return render(request, 'role_app/permission_denied.html', status=403)


def home(request):
    """Public home page."""
    return render(request, 'role_app/home.html')


def user_login(request):
    """Login view using Django AuthenticationForm with dynamic role redirection."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'role_app/login.html', {'form': form})


@login_required
def user_logout(request):
    """Logout view."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def dashboard(request):
    """Dynamic dashboard based on Django Group membership."""
    user = request.user
    user_groups = set(user.groups.values_list('name', flat=True))

    is_seller = 'Seller' in user_groups
    is_buyer = 'Buyer' in user_groups
    is_critic = 'MovieCritic' in user_groups
    is_fan = 'MovieFan' in user_groups
    is_admin = 'Admin' in user_groups
    has_no_role = not (is_seller or is_buyer or is_critic or is_fan or is_admin or user.is_superuser)

    context = {
        'is_seller': is_seller,
        'is_buyer': is_buyer,
        'is_critic': is_critic,
        'is_fan': is_fan,
        'is_admin': is_admin,
        'has_no_role': has_no_role,
        'user_groups': list(user_groups),
    }

    if is_seller:
        seller_products = Product.objects.filter(seller=user)
        context['seller_products'] = seller_products
        context['product_count'] = seller_products.count()
        context['recent_products'] = seller_products[:5]

    if is_buyer:
        user_orders = Order.objects.filter(user=user)
        context['buyer_orders'] = user_orders
        context['order_count'] = user_orders.count()
        context['available_products'] = Product.objects.all()[:6]

    return render(request, 'role_app/dashboard.html', context)


@login_required
def my_orders(request):
    """Display orders belonging ONLY to the currently logged in user."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'role_app/orders.html', {'orders': orders})


@permission_required('role_app.add_product', raise_exception=True)
def post_product(request):
    """Post product page accessible only to users with add_product permission (Sellers)."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f"Product '{product.name}' posted successfully!")
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'role_app/post_product.html', {'form': form})


@permission_required('role_app.view_product', raise_exception=True)
def product_list(request):
    """View products list page."""
    products = Product.objects.all()
    can_buy_product = request.user.has_perm('role_app.add_order')
    return render(request, 'role_app/products.html', {
        'products': products,
        'can_buy_product': can_buy_product
    })


@permission_required('role_app.add_order', raise_exception=True)
def buy_product(request, product_id):
    """Purchase a product and create a new order for the logged in user."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        Order.objects.create(
            user=request.user,
            product_name=product.name,
            price=product.price,
            status='Completed'
        )
        messages.success(request, f"Order placed successfully for '{product.name}'!")
        return redirect('my_orders')
    return redirect('product_list')



@permission_required('role_app.view_movie', raise_exception=True)
def movie_list(request):
    """View movies page."""
    movies = Movie.objects.all()
    can_add_review = request.user.has_perm('role_app.add_review')
    return render(request, 'role_app/movies.html', {
        'movies': movies,
        'can_add_review': can_add_review
    })


@permission_required('role_app.view_review', raise_exception=True)
def review_list(request):
    """View reviews page."""
    reviews = Review.objects.all()
    can_add_review = request.user.has_perm('role_app.add_review')
    can_change_review = request.user.has_perm('role_app.change_review')
    return render(request, 'role_app/reviews.html', {
        'reviews': reviews,
        'can_add_review': can_add_review,
        'can_change_review': can_change_review,
    })


@permission_required('role_app.add_review', raise_exception=True)
def add_review(request):
    """Add review view, restricted to users with add_review permission (MovieCritic)."""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Review published successfully!")
            return redirect('review_list')
    else:
        form = ReviewForm()

    return render(request, 'role_app/add_review.html', {'form': form})


@permission_required('role_app.change_review', raise_exception=True)
def edit_review(request, review_id):
    """Edit review view, restricted to users with change_review permission (MovieCritic)."""
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully!")
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'role_app/edit_review.html', {'form': form, 'review': review})


@login_required
def playlist_admin_view(request):
    """Playlist Admin view restricted to members of the Admin group."""
    if not request.user.groups.filter(name='Admin').exists():
        raise PermissionDenied("You do not belong to the Admin group.")

    playlists = Playlist.objects.all()
    return render(request, 'role_app/playlist_admin.html', {'playlists': playlists})
