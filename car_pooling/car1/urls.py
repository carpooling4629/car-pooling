from django.urls import path, include
from . import views
urlpatterns = [
    path(r'', views.signin),
    path(r'signin/', views.signin),
    path(r'signup/',views.signup),
    path(r'profile/update/',views.update),
    path(r'forgot_password/',views.forgot_password),
    path(r'signout/',views.signout),
    path(r'home/',views.home),
    # path(r'home/lift/', views.lift),
    # path(r'home/trip/', views.trip),
    path(r'profile/',views.display_profile),
    path(r'home/cancelTrip/',views.cancel_ride_request),
    path(r'firebase/', views.firebase1),
    path(r'home/cancelLift/',views.cancel_ride_request),
    path(r'home/userList/',views.user_list),
    path(r'home/acceptTrip/',views.accept_lift_request)
]