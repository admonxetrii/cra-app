from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
                  path('', views.signin, name='signin'),
                  path('signout/', views.signout, name='signout'),
                  path('register/', views.signup, name='register'),
                  path('dashboard/', views.dashboard, name='dashboard'),
                  path('table/', views.tables, name='table'),
                  path('reservations/', views.reservations, name='reservations'),
                  path('approve-reservation/<int:id>', views.approve_reservation, name='approve-reservation'),
                  path('cancel-reservation/<int:id>', views.cancel_reservation, name='cancel-reservation'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
