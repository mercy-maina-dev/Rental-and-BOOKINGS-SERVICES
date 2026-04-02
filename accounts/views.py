# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .decorators import tenant_required, landlord_required


# ── Register ──────────────────────────────────────────────
# accounts/views.py — update register_view only

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # grab role from the hidden tab input
            role = request.POST.get('role', 'tenant')
            if role not in ['tenant', 'landlord']:
                role = 'tenant'
            user.role = role
            user.save()
            login(request, user)
            messages.success(
                request, f'Welcome {user.username}! Your {role} account is ready.')
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

# ── Login ─────────────────────────────────────────────────


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    # detect which portal tab was selected
    selected_role = request.POST.get(
        'selected_role', request.GET.get('role', 'tenant'))

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            role = request.POST.get('selected_role', 'tenant')

            # Block wrong portal
            if role == 'tenant' and not user.is_tenant:
                messages.error(
                    request, 'This login portal is for tenants only. Use the Landlord portal.')
                return render(request, 'accounts/login.html', {'form': form, 'selected_role': role})

            if role == 'landlord' and not user.is_landlord:
                messages.error(
                    request, 'This login portal is for landlords only. Use the Tenant portal.')
                return render(request, 'accounts/login.html', {'form': form, 'selected_role': role})

            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'selected_role': selected_role})


# ── Logout ────────────────────────────────────────────────
def logout_view(request):
    username = request.user.username
    logout(request)
    messages.success(request, f'Goodbye {username}! You have been logged out.')
    return redirect('login')


# ── Profile ───────────────────────────────────────────────
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


# ── Dashboard Redirect ────────────────────────────────────
@login_required
def dashboard_redirect(request):
    if request.user.is_landlord:
        return redirect('landlord_dashboard')
    elif request.user.is_admin_user:
        return redirect('admin_dashboard')
    else:
        return redirect('tenant_dashboard')
