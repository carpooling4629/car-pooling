from django.urls import path, include
from . import views
urlpatterns = [
    path(r'', views.signin),
    path(r'signin/', views.signin),
    path(r'signup/',views.signup),
    path(r'update_profile/',views.update),
    path(r'forgot_password/',views.forgot_password),
    path(r'signout/',views.signout),
    path(r'home/',views.home),
    path(r'home/lift/', views.lift),
    path(r'home/trip/', views.trip),
    path(r'home/cancelTrip/',views.cancel_ride_request),
    path(r'home/acceptTrip/',views.accept_lift_request)
]