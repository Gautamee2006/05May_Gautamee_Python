from django.shortcuts import render
from .models import Offer
from datetime import date

def offers_list_view(request):
    offers = Offer.objects.filter(is_active=True, end_date__gte=date.today()).select_related('restaurant')
    return render(request, 'offers/offers_list.html', {'offers': offers})
