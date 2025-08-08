from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Trip Management
    path('trip/add/', views.add_trip, name='add_trip'),
    path('trip/delete/<int:trip_id>/', views.delete_trip, name='delete_trip'),

    # Expense Management
    path('trip/<int:trip_id>/expenses/', views.manage_expenses, name='manage_expenses'),
    path('expense/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]
