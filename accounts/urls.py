from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('dashboard/', views.dashboard, name='accounts.dashboard'),
    path('dashboard/top-buyer/', views.top_buyer, name='accounts.top_buyer'),
    path('dashboard/buyers/', views.buyers_list, name='accounts.buyers_list'),
    path('dashboard/top-commenter/', views.top_commenter, name='accounts.top_commenter')
]