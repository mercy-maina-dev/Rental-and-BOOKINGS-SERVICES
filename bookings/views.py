# bookings/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import tenant_required, landlord_required
from houses.models import House
from .models import Booking
from .forms import BookingForm


# ── Tenant: Book a house ──────────────────────────────────
@tenant_required
def book_house(request, pk):
    house = get_object_or_404(House, pk=pk)

    if not house.is_available:
        messages.error(request, 'This house is not available for booking.')
        return redirect('house_detail', pk=pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']

            # ── Double-booking check ──────────────────────
            clash = Booking.objects.filter(
                house=house,
                status__in=['pending', 'approved'],
            ).filter(
                start_date__lt=end,
                end_date__gt=start,
            ).exists()

            if clash:
                messages.error(
                    request,
                    'These dates overlap with an existing booking. '
                    'Please choose different dates.'
                )
                return render(request, 'bookings/book_house.html',
                              {'form': form, 'house': house})

            booking = form.save(commit=False)
            booking.tenant = request.user
            booking.house = house
            booking.save()

            messages.success(
                request,
                f'Booking request for "{house.title}" submitted! '
                f'Waiting for landlord approval.'
            )
            return redirect('my_bookings')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = BookingForm()

    return render(request, 'bookings/book_house.html',
                  {'form': form, 'house': house})


# ── Tenant: My bookings ───────────────────────────────────
@tenant_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        tenant=request.user
    ).order_by('-created_at')

    # filter by status tab
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)

    counts = {
        'all': Booking.objects.filter(tenant=request.user).count(),
        'pending': Booking.objects.filter(tenant=request.user, status='pending').count(),
        'approved': Booking.objects.filter(tenant=request.user, status='approved').count(),
        'rejected': Booking.objects.filter(tenant=request.user, status='rejected').count(),
        'cancelled': Booking.objects.filter(tenant=request.user, status='cancelled').count(),
    }

    return render(request, 'bookings/my_bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter,
        'counts': counts,
    })


# ── Tenant: Cancel booking ────────────────────────────────
@tenant_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, tenant=request.user)

    if booking.status not in ['pending', 'approved']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('my_bookings')

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(
            request, f'Booking for "{booking.house.title}" has been cancelled.')
        return redirect('my_bookings')

    return render(request, 'bookings/cancel_confirm.html', {'booking': booking})


# ── Landlord: Manage bookings for a house ────────────────
@landlord_required
def manage_bookings(request, pk):
    house = get_object_or_404(House, pk=pk, landlord=request.user)
    bookings = Booking.objects.filter(house=house).order_by('-created_at')

    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        bookings = bookings.filter(status=status_filter)

    counts = {
        'all': Booking.objects.filter(house=house).count(),
        'pending': Booking.objects.filter(house=house, status='pending').count(),
        'approved': Booking.objects.filter(house=house, status='approved').count(),
        'rejected': Booking.objects.filter(house=house, status='rejected').count(),
    }

    return render(request, 'bookings/manage_bookings.html', {
        'house': house,
        'bookings': bookings,
        'status_filter': status_filter,
        'counts': counts,
    })


# ── Landlord: Approve booking ─────────────────────────────
@landlord_required
def approve_booking(request, pk):
    booking = get_object_or_404(
        Booking, pk=pk, house__landlord=request.user)

    if booking.status != 'pending':
        messages.error(request, 'Only pending bookings can be approved.')
        return redirect('manage_bookings', pk=booking.house.pk)

    if request.method == 'POST':
        booking.status = 'approved'
        booking.save()

        # mark house as booked
        booking.house.availability = 'booked'
        booking.house.save()

        messages.success(
            request,
            f'Booking by {booking.tenant.username} has been approved!'
        )
        return redirect('manage_bookings', pk=booking.house.pk)

    return render(request, 'bookings/approve_confirm.html', {'booking': booking})


# ── Landlord: Reject booking ──────────────────────────────
@landlord_required
def reject_booking(request, pk):
    booking = get_object_or_404(
        Booking, pk=pk, house__landlord=request.user)

    if booking.status != 'pending':
        messages.error(request, 'Only pending bookings can be rejected.')
        return redirect('manage_bookings', pk=booking.house.pk)

    if request.method == 'POST':
        booking.status = 'rejected'
        booking.save()
        messages.success(
            request,
            f'Booking by {booking.tenant.username} has been rejected.'
        )
        return redirect('manage_bookings', pk=booking.house.pk)

    return render(request, 'bookings/reject_confirm.html', {'booking': booking})
