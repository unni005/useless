from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Trip, Expense
from .forms import TripForm, ExpenseForm

# --------------------------
# User Registration
# --------------------------
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'register.html')

# --------------------------
# User Login
# --------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

# --------------------------
# User Logout
# --------------------------
def logout_view(request):
    logout(request)
    return redirect('login')

# --------------------------
# Dashboard - List Trips
# --------------------------
@login_required
def dashboard(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'trips': trips})

# --------------------------
# Add a Trip
# --------------------------
@login_required
def add_trip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            return redirect('dashboard')
    else:
        form = TripForm()
    return render(request, 'add_trip.html', {'form': form})

# --------------------------
# Delete a Trip
# --------------------------
@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    trip.delete()
    return redirect('dashboard')

# --------------------------
# Manage Expenses for a Trip
# --------------------------
@login_required
def manage_expenses(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    expenses = Expense.objects.filter(trip=trip)

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.trip = trip
            expense.save()
            return redirect('manage_expenses', trip_id=trip.id)
    else:
        form = ExpenseForm()

    return render(request, 'manage_expenses.html', {
        'trip': trip,
        'expenses': expenses,
        'form': form
    })

# --------------------------
# Delete an Expense
# --------------------------
@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, trip__user=request.user)
    trip_id = expense.trip.id
    expense.delete()
    return redirect('manage_expenses', trip_id=trip_id)
