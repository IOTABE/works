from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ServiceOffer, ServiceRequest, Category
from .forms import ServiceOfferForm, ServiceRequestForm

def home(request):
    filter_type = request.GET.get('type', 'all')
    search_query = request.GET.get('q', '')
    category_slug = request.GET.get('category', 'all')

    offers = ServiceOffer.objects.filter(is_active=True)
    requests = ServiceRequest.objects.filter(is_active=True)

    if search_query:
        offers = offers.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        requests = requests.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
        
    if category_slug != 'all':
        offers = offers.filter(category__slug=category_slug)
        requests = requests.filter(category__slug=category_slug)

    offers = offers.order_by('-created_at')
    requests = requests.order_by('-created_at')

    items = []
    if filter_type in ['all', 'offers']:
        for o in offers:
            items.append({'type': 'offer', 'item': o, 'date': o.created_at})
    if filter_type in ['all', 'requests']:
        for r in requests:
            items.append({'type': 'request', 'item': r, 'date': r.created_at})
    
    # Sort by date descending
    items.sort(key=lambda x: x['date'], reverse=True)

    categories = Category.objects.all()

    context = {
        'items': items,
        'filter_type': filter_type,
        'search_query': search_query,
        'category_slug': category_slug,
        'categories': categories
    }

    if request.htmx:
        return render(request, 'services/partials/feed_list.html', context)
    
    return render(request, 'services/home.html', context)

@login_required
def create_offer(request):
    if not request.user.is_professional:
        return redirect('home')
        
    if request.method == 'POST':
        form = ServiceOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.professional = request.user.professional_profile
            offer.save()
            return redirect('home')
    else:
        form = ServiceOfferForm()
        
    return render(request, 'services/create_offer.html', {'form': form})

@login_required
def create_request(request):
    if not request.user.is_client:
        return redirect('home')
        
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.client = request.user.client_profile
            service_request.save()
            return redirect('home')
    else:
        form = ServiceRequestForm()
        
    return render(request, 'services/create_request.html', {'form': form})

@login_required
def my_services(request):
    items = []
    if request.user.is_professional:
        offers = ServiceOffer.objects.filter(professional=request.user.professional_profile, is_active=True).order_by('-created_at')
        for o in offers:
            items.append({'type': 'offer', 'item': o})
    
    if request.user.is_client:
        requests = ServiceRequest.objects.filter(client=request.user.client_profile, is_active=True).order_by('-created_at')
        for r in requests:
            items.append({'type': 'request', 'item': r})
            
    return render(request, 'services/my_services.html', {'items': items})

@login_required
def delete_service(request, pk, type_service):
    if type_service == 'offer':
        service = get_object_or_404(ServiceOffer, pk=pk, professional=request.user.professional_profile)
    else:
        service = get_object_or_404(ServiceRequest, pk=pk, client=request.user.client_profile)
        
    if request.method == 'POST':
        # Em vez de apagar, vamos desativar
        service.is_active = False
        service.save()
        return redirect('my_services')
        
    return redirect('my_services')
