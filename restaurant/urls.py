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
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
