# houses/views.py

from django.shortcuts import render, get_object_or_404, redirect
from accounts.decorators import landlord_required, tenant_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import House
from .forms import HouseForm, HouseSearchForm


# ── Public: Browse all available houses ──────────────────
def house_list(request):
    houses = House.objects.filter(
        availability='available').order_by('-created_at')
    form = HouseSearchForm(request.GET)

    if form.is_valid():
        q = form.cleaned_data.get('q')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        bedrooms = form.cleaned_data.get('bedrooms')

        if q:
            houses = houses.filter(title__icontains=q) | \
                House.objects.filter(location__icontains=q,
                                     availability='available')
            houses = houses.distinct()
        if min_price:
            houses = houses.filter(price__gte=min_price)
        if max_price:
            houses = houses.filter(price__lte=max_price)
        if bedrooms:
            houses = houses.filter(bedrooms=bedrooms)

    paginator = Paginator(houses, 9)
    page = request.GET.get('page')
    houses = paginator.get_page(page)

    return render(request, 'houses/house_list.html', {
        'houses': houses,
        'form': form,
    })


# ── Public: House detail ──────────────────────────────────
def house_detail(request, pk):
    house = get_object_or_404(House, pk=pk)
    return render(request, 'houses/house_detail.html', {'house': house})


# ── Landlord: Add house ───────────────────────────────────
@landlord_required
def house_add(request):
    if not request.user.is_landlord:
        messages.error(request, 'Only landlords can add listings.')
        return redirect('house_list')

    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            house = form.save(commit=False)
            house.landlord = request.user
            house.save()
            messages.success(
                request, f'"{house.title}" has been listed successfully!')
            return redirect('landlord_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = HouseForm()

    return render(request, 'houses/house_form.html', {'form': form, 'action': 'Add'})


# ── Landlord: Edit house ──────────────────────────────────
@landlord_required
def house_edit(request, pk):
    house = get_object_or_404(House, pk=pk, landlord=request.user)

    if request.method == 'POST':
        form = HouseForm(request.POST, request.FILES, instance=house)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{house.title}" updated successfully!')
            return redirect('landlord_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = HouseForm(instance=house)

    return render(request, 'houses/house_form.html', {'form': form, 'action': 'Edit', 'house': house})


# ── Landlord: Delete house ────────────────────────────────
@landlord_required
def house_delete(request, pk):
    house = get_object_or_404(House, pk=pk, landlord=request.user)

    if request.method == 'POST':
        title = house.title
        house.delete()
        messages.success(request, f'"{title}" has been removed.')
        return redirect('landlord_dashboard')

    return render(request, 'houses/house_confirm_delete.html', {'house': house})


# ── Landlord: Dashboard ───────────────────────────────────
@landlord_required
def landlord_dashboard(request):
    if not request.user.is_landlord:
        messages.error(request, 'Access denied.')
        return redirect('house_list')

    houses = House.objects.filter(
        landlord=request.user).order_by('-created_at')

    # stats
    from bookings.models import Booking
    total_bookings = Booking.objects.filter(
        house__landlord=request.user).count()
    pending_count = Booking.objects.filter(
        house__landlord=request.user, status='pending').count()
    approved_count = Booking.objects.filter(
        house__landlord=request.user, status='approved').count()
    recent_bookings = Booking.objects.filter(
        house__landlord=request.user).order_by('-created_at')[:5]

    return render(request, 'houses/landlord_dashboard.html', {
        'houses': houses,
        'total_bookings': total_bookings,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'recent_bookings': recent_bookings,
    })


# ── Tenant: Dashboard ─────────────────────────────────────
@tenant_required
def tenant_dashboard(request):
    if not request.user.is_tenant:
        messages.error(request, 'Access denied.')
        return redirect('house_list')

    from bookings.models import Booking
    bookings = Booking.objects.filter(
        tenant=request.user).order_by('-created_at')
    pending_count = bookings.filter(status='pending').count()
    approved_count = bookings.filter(status='approved').count()

    return render(request, 'houses/tenant_dashboard.html', {
        'bookings': bookings[:5],
        'pending_count': pending_count,
        'approved_count': approved_count,
        'total': bookings.count(),
    })
