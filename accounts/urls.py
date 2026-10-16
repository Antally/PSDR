from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',   auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/',  auth_views.LogoutView.as_view(next_page='core:home'),              name='logout'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/driver/',     views.register_driver,     name='register_driver'),
    path('register/owner/',      views.register_owner,      name='register_owner'),
    path('register/event-host/', views.register_event_host, name='register_event_host'),
]