from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Category, Product, ProductImage, Review
from .forms import ReviewForm
from accounts.models import RecentlyViewed
from orders.models import Order, OrderItem

def home_view(request):
    categories = Category.objects.all()[:8]
    featured_products = Product.objects.filter(is_active=True).order_by('-rating')[:8]
    trending_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    discount_offers = Product.objects.filter(is_active=True, discount_percentage__gte=15).order_by('-discount_percentage')[:8]
    best_sellers = Product.objects.filter(is_active=True, stock__gt=0).order_by('stock')[:8]

    # Recommendations logic: Based on recently viewed category or high rating
    recommended_products = Product.objects.filter(is_active=True).order_by('?')[:8]
    recently_viewed_items = []
    
    if request.user.is_authenticated:
        recent_entries = RecentlyViewed.objects.filter(user=request.user)[:8]
        recently_viewed_items = [entry.product for entry in recent_entries]
        if recent_entries.exists():
            last_category = recent_entries.first().product.category
            recommended_products = Product.objects.filter(is_active=True, category=last_category).exclude(id=recent_entries.first().product.id)[:8]

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'trending_products': trending_products,
        'discount_offers': discount_offers,
        'best_sellers': best_sellers,
        'recommended_products': recommended_products,
        'recently_viewed_products': recently_viewed_items,
    }
    return render(request, 'home.html', context)


def product_list_view(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Search & Filters
    category_slug = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('rating')
    in_stock = request.GET.get('in_stock')
    sort_by = request.GET.get('sort')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if min_price:
        try:
            products = products.filter(final_price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(final_price__lte=float(max_price))
        except ValueError:
            pass

    if min_rating:
        try:
            products = products.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    if in_stock == '1':
        products = products.filter(stock__gt=0)

    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('final_price')
    elif sort_by == 'price_high':
        products = products.order_by('-final_price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    elif sort_by == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'in_stock': in_stock,
        'sort_by': sort_by,
    }
    return render(request, 'products/product_list.html', context)


def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)

    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('final_price')
    elif sort_by == 'price_high':
        products = products.order_by('-final_price')
    elif sort_by == 'rating':
        products = products.order_by('-rating')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'sort_by': sort_by
    }
    return render(request, 'products/category.html', context)


def search_view(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'products/search.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    reviews = product.reviews.select_related('user').order_by('-created_at')

    # Track recently viewed
    if request.user.is_authenticated:
        RecentlyViewed.objects.update_or_create(
            user=request.user,
            product=product
        )

    # Check if user can review (must have ordered and order status == 'Delivered')
    can_review = False
    delivered_order = None
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user, order_status='Delivered')
        delivered_items = OrderItem.objects.filter(order__in=user_orders, product=product)
        if delivered_items.exists():
            delivered_order = delivered_items.first().order
            # Check if review already submitted for this order
            if not Review.objects.filter(product=product, user=request.user, order=delivered_order).exists():
                can_review = True

    review_form = ReviewForm()

    # Related / Recommended products
    related_products = Product.objects.filter(
        Q(category=product.category) | Q(brand=product.brand),
        is_active=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'can_review': can_review,
        'review_form': review_form,
        'delivered_order': delivered_order,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        # Verify user has delivered order
        user_orders = Order.objects.filter(user=request.user, order_status='Delivered')
        delivered_item = OrderItem.objects.filter(order__in=user_orders, product=product).first()

        if not delivered_item:
            messages.error(request, "You can only review products that have been delivered to you.")
            return redirect('products:product_detail', slug=product.slug)

        order = delivered_item.order

        if Review.objects.filter(product=product, user=request.user, order=order).exists():
            messages.warning(request, "You have already reviewed this product for this order.")
            return redirect('products:product_detail', slug=product.slug)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.order = order
            review.save()
            messages.success(request, "Thank you! Your review has been published.")
        else:
            messages.error(request, "Error submitting review. Please check inputs.")

    return redirect('products:product_detail', slug=product.slug)
