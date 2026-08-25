from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SupportTicket, FAQ
from .forms import SupportTicketForm

def faq_view(request):
    faqs = FAQ.objects.filter(is_active=True)
    categories = ['Account', 'Orders', 'Payments', 'Returns', 'Delivery', 'Coupons']
    
    categorized_faqs = {}
    for cat in categories:
        categorized_faqs[cat] = faqs.filter(category=cat)

    return render(request, 'support/faq.html', {'categorized_faqs': categorized_faqs})


@login_required
def contact_view(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, f"Support ticket #{ticket.ticket_id} submitted! Our support team will get back to you shortly.")
            return redirect('support:tickets')
    else:
        form = SupportTicketForm()

    return render(request, 'support/contact.html', {'form': form})


@login_required
def tickets_list_view(request):
    tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, 'support/tickets.html', {'tickets': tickets})
